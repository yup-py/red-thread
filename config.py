"""
Bronze ingestion config — one entry per source file.
Add new sources here without touching extract_load.py.
"""

RAW_DIR = "data/raw"

HOLLYWOOD_COLUMNS = [
    "title", "date", "genre", "orig_lang",
    "revenue_usd", "budget_usd", "country", "score",
]

SOURCES = {
    "netflix": {
        "file": "Netflix.csv",
        "table": "RAW_NETFLIX",
        "has_header": True,
    },
    "amazon_prime": {
        "file": "amazon_prime_titles.csv",
        "table": "RAW_AMAZON_PRIME",
        "has_header": True,
    },
    "apple": {
        "file": "apple.csv",
        "table": "RAW_APPLE",
        "has_header": True,
    },
    "hotstar": {
        "file": "hotstar.csv",
        "table": "RAW_HOTSTAR",
        "has_header": True,
    },
    "bollywood": {
        "file": "Final Bollywood.csv",
        "table": "RAW_BOLLYWOOD",
        "has_header": True,
    },
    "hollywood": {
        "file": "Final Hollywood.csv",
        "table": "RAW_HOLLYWOOD",
        "has_header": False,          # <- the data quality anomaly from the cahier des charges
        "column_names": HOLLYWOOD_COLUMNS,
    },
}
