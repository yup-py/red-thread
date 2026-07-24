import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

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
        "has_header": False,
    },
}