import argparse
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
from dotenv import load_dotenv

from ingestion.source_configs import SOURCES, RAW_DIR
from utils.pipeline_logger import get_logger

load_dotenv()

REQUIRED_SNOWFLAKE_VARS = [
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_PASSWORD",
    "SNOWFLAKE_WAREHOUSE",
    "SNOWFLAKE_DATABASE",
]


def ensure_snowflake_ready():
    """Auto-initialize Snowflake warehouse, database, and dbt layer schemas."""
    log = get_logger("init")

    missing = [v for v in REQUIRED_SNOWFLAKE_VARS if v not in os.environ]
    if missing:
        log.error(f"Missing required env vars: {missing}")
        sys.exit(1)

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

        log.info(f"Ensuring warehouse '{warehouse}' exists...")
        cursor.execute(
            f"CREATE WAREHOUSE IF NOT EXISTS {warehouse} "
            "WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE"
        )
        cursor.execute(f"USE WAREHOUSE {warehouse}")

        log.info(f"Ensuring database '{database}' exists...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cursor.execute(f"USE DATABASE {database}")

        dbt_schemas = ["RAW", "STAGING", "INTERMEDIATE", "MARTS"]
        for schema in dbt_schemas:
            log.info(f"Ensuring schema '{schema}' exists...")
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")

        log.info(
            f"Snowflake infrastructure verified "
            f"({warehouse} -> {database} -> RAW / STAGING / INTERMEDIATE / MARTS)"
        )

        cursor.close()
        conn.close()
    except Exception as e:
        log.error(f"Snowflake init FAILED: {e}")
        sys.exit(1)


def read_source(name: str, cfg: dict) -> pd.DataFrame:
    log = get_logger(name)
    path = os.path.join(RAW_DIR, cfg["file"])

    if not os.path.exists(path):
        log.error(f"Expected file at {path} — ensure CSV files are copied into {RAW_DIR}/")
        raise FileNotFoundError(
            f"[{name}] expected file at {path} — ensure CSV files are copied into {RAW_DIR}/"
        )

    try:
        if cfg["has_header"]:
            df = pd.read_csv(path, encoding="utf-8")
        else:
            df = pd.read_csv(path, encoding="utf-8", header=None)
            df.columns = [f"column_{i}" for i in range(len(df.columns))]
    except UnicodeDecodeError:
        log.warning("UTF-8 decode failed, retrying with latin-1 encoding")
        if cfg["has_header"]:
            df = pd.read_csv(path, encoding="latin-1")
        else:
            df = pd.read_csv(path, encoding="latin-1", header=None)
            df.columns = [f"column_{i}" for i in range(len(df.columns))]

    log.info(f"Loaded {len(df)} rows, {len(df.columns)} columns from {path}")
    return df


def load_to_snowflake(name: str, table: str, df: pd.DataFrame):
    import snowflake.connector
    from snowflake.connector.pandas_tools import write_pandas

    log = get_logger(name)
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
        source_row_count = len(df)

        # Standardize column headers to upper-case valid Snowflake identifiers
        df.columns = [c.strip().upper().replace(" ", "_").replace("-", "_") for c in df.columns]

        log.info(f"Writing {source_row_count} rows to {raw_schema}.{table.upper()}...")
        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name=table.upper(),
            database=os.environ["SNOWFLAKE_DATABASE"],
            schema=raw_schema,
            auto_create_table=True,
            overwrite=True,
        )

        log.info(f"-> Snowflake {raw_schema}.{table.upper()}: success={success}, rows={nrows}, chunks={nchunks}")

        if nrows != source_row_count:
            log.warning(
                f"Row count mismatch: source had {source_row_count} rows, "
                f"Snowflake reports {nrows} rows loaded"
            )
    finally:
        conn.close()


def run_source(name: str, to_snowflake: bool = True):
    log = get_logger(name)
    cfg = SOURCES[name]
    df = read_source(name, cfg)
    if to_snowflake:
        load_to_snowflake(name, cfg["table"], df)
    log.info(f"Finished processing source '{name}'")
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

    pipeline_log = get_logger("pipeline")
    pipeline_log.info(f"Run started (all={args.all}, source={args.source}, no_load={args.no_load})")

    if not args.no_load:
        ensure_snowflake_ready()

    targets = list(SOURCES.keys()) if args.all else [args.source]

    succeeded, failed = [], []
    for name in targets:
        try:
            run_source(name, to_snowflake=not args.no_load)
            succeeded.append(name)
        except Exception as e:
            log = get_logger(name)
            log.error(f"FAILED: {e}")
            failed.append(name)
            if not args.all:
                pipeline_log.error(f"Run aborted due to failure in '{name}'")
                sys.exit(1)

    pipeline_log.info(f"Run finished. Succeeded: {succeeded}. Failed: {failed}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()