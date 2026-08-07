
import logging
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_ROOT = os.environ.get("LOG_DIR", os.path.join(BASE_DIR, "logs"))

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_configured_loggers = {}


def get_logger(step_name: str) -> logging.Logger:

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
