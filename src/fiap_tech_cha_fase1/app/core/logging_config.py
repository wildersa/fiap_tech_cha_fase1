# app/core/logging_config.py
import logging.config
import os
from pathlib import Path
import sys

# Resolve caminho absoluto do log
PROJECT_ROOT = Path(__file__).resolve().parents[2]   # ajuste conforme a profundidade
LOG_DIR = Path(os.getenv("APP_LOG_DIR", PROJECT_ROOT / "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

APP_NAME = os.getenv("APP_NAME")
LOG_FILE = LOG_DIR / f"{APP_NAME}.log"

# Configuração central de logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_FILE),
            "formatter": "json",
        },
    },
    "root": {"handlers": ["stdout", "file"], "level": "INFO"},
}

def setup_logging():
    logging.config.dictConfig(LOGGING)
