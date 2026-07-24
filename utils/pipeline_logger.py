"""
pipeline_logger.py

Central logging utility for the ELT pipeline.

Folder layout produced:

    logs/
      <step_name>/
        YYYY-MM-DD.log     <- all log lines for that step, that day (appended across runs)

Usage:
    from pipeline_logger import get_logger

    log = get_logger("netflix")     # step-specific logger -> logs/netflix/2026-07-24.log
    log.info("loaded 5331 rows")

    log = get_logger("pipeline")    # overall run logger    -> logs/pipeline/2026-07-24.log
    log = get_logger("init")        # snowflake init logger  -> logs/init/2026-07-24.log

Each logger also echoes to the console (stdout) so behavior in the terminal
is unchanged, in addition to being written to disk.
"""

import logging
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_ROOT = os.environ.get("LOG_DIR", os.path.join(BASE_DIR, "logs"))

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_configured_loggers = {}


def get_logger(step_name: str) -> logging.Logger:
    """
    Return a logger for a given pipeline step (e.g. a source name like
    'netflix', or a lifecycle step like 'init' / 'pipeline').

    Creates logs/<step_name>/ if it doesn't exist, and writes to a file
    named after today's date inside it. Multiple runs on the same day
    append to the same file.
    """
    if step_name in _configured_loggers:
        return _configured_loggers[step_name]

    step_dir = os.path.join(LOG_ROOT, step_name)
    os.makedirs(step_dir, exist_ok=True)

    log_file = os.path.join(step_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

    logger = logging.getLogger(f"pipeline.{step_name}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    # File handler -> logs/<step_name>/<today>.log
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    _configured_loggers[step_name] = logger
    return logger
