
import argparse
import os
import sys
import pandas as pd
from dotenv import load_dotenv

from source_configs import SOURCES, RAW_DIR

load_dotenv()


def ensure_snowflake_ready():
    """Auto-initialize Snowflake warehouse, database, and dbt layer schemas."""
    try:
        import snowflake.connector

        conn_params = {
            "account": os.environ["SNOWFLAKE_ACCOUNT"],
            "user": os.environ["SNOWFLAKE_USER"],
            "password": os.environ["SNOWFLAKE_PASSWORD"],
        }
        if os.environ.get("SNOWFLAKE_ROLE"):
            conn_params["role"] = os.environ["SNOWFLAKE_ROLE"]

        conn = snowflake.connector.connect(**conn_params)
        cursor = conn.cursor()

        warehouse = os.environ["SNOWFLAKE_WAREHOUSE"]
        database = os.environ["SNOWFLAKE_DATABASE"]

        # Ensure Warehouse exists
        print(f"[Init] Ensuring warehouse '{warehouse}' exists...")
        cursor.execute(
            f"CREATE WAREHOUSE IF NOT EXISTS {warehouse} "
            "WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE"
        )
        cursor.execute(f"USE WAREHOUSE {warehouse}")

        # Ensure Database exists
        print(f"[Init] Ensuring database '{database}' exists...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cursor.execute(f"USE DATABASE {database}")

        # Ensure Schemas exist matching dbt model folders
        dbt_schemas = ["RAW", "STAGING", "INTERMEDIATE", "MARTS"]
        for schema in dbt_schemas:
            print(f"[Init] Ensuring schema '{schema}' exists...")
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")

        print(f"[Init] ✓ Snowflake infrastructure verified ({warehouse} -> {database} -> RAW / STAGING / INTERMEDIATE / MARTS)")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[Init] FAILED: {e}", file=sys.stderr)
        sys.exit(1)


def read_source(name: str, cfg: dict) -> pd.DataFrame:
    path = os.path.join(RAW_DIR, cfg["file"])
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"[{name}] expected file at {path} — ensure CSV files are copied into {RAW_DIR}/"
        )

    if cfg["has_header"]:
        df = pd.read_csv(path, encoding="utf-8")
    else:
        df = pd.read_csv(path, encoding="utf-8", header=None)
        df.columns = [f"column_{i}" for i in range(len(df.columns))]

    print(f"[{name}] loaded {len(df)} rows, {len(df.columns)} columns from {path}")
    return df


def load_to_snowflake(name: str, table: str, df: pd.DataFrame):
    import snowflake.connector
    from snowflake.connector.pandas_tools import write_pandas

    raw_schema = os.environ.get("SNOWFLAKE_RAW_SCHEMA", "RAW")

    conn_params = {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "password": os.environ["SNOWFLAKE_PASSWORD"],
        "warehouse": os.environ["SNOWFLAKE_WAREHOUSE"],
        "database": os.environ["SNOWFLAKE_DATABASE"],
        "schema": raw_schema,
    }
    if os.environ.get("SNOWFLAKE_ROLE"):
        conn_params["role"] = os.environ["SNOWFLAKE_ROLE"]

    conn = snowflake.connector.connect(**conn_params)
    try:
        # Standardize column headers to upper-case valid Snowflake identifiers
        df.columns = [c.strip().upper().replace(" ", "_").replace("-", "_") for c in df.columns]

        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name=table.upper(),
            database=os.environ["SNOWFLAKE_DATABASE"],
            schema=raw_schema,
            auto_create_table=True,
            overwrite=True,
        )
        print(f"[{name}] -> Snowflake {raw_schema}.{table.upper()}: success={success}, rows={nrows}")
    finally:
        conn.close()


def run_source(name: str, to_snowflake: bool = True):
    cfg = SOURCES[name]
    df = read_source(name, cfg)
    if to_snowflake:
        load_to_snowflake(name, cfg["table"], df)
    return df


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source", choices=SOURCES.keys(), help="run a single source")
    group.add_argument("--all", action="store_true", help="run every source")
    parser.add_argument(
        "--no-load",
        action="store_true",
        help="only read/validate local CSV, skip Snowflake load",
    )
    args = parser.parse_args()

    if not args.no_load:
        ensure_snowflake_ready()

    targets = list(SOURCES.keys()) if args.all else [args.source]

    for name in targets:
        try:
            run_source(name, to_snowflake=not args.no_load)
        except Exception as e:
            print(f"[{name}] FAILED: {e}", file=sys.stderr)
            if not args.all:
                sys.exit(1)


if __name__ == "__main__":
    main()