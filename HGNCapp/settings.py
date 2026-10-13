import os
from pathlib import Path

# --------------------------------------------------
# STEP 1: Define default log file
# --------------------------------------------------
home_dir = os.path.expanduser(".")
DEFAULT_LOG = os.path.join(home_dir, "HGNC_app.log")

LOG_FILE = DEFAULT_LOG


# --------------------------------------------------
# STEP 2: NORMALISE the path (defensive step)
# --------------------------------------------------
LOG_FILE = os.path.abspath(os.path.expanduser(LOG_FILE))


# --------------------------------------------------
# STEP 3: Ensure directory exists
# --------------------------------------------------
log_dir = os.path.dirname(LOG_FILE)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)


# --------------------------------------------------
# STEP 4: Logging configuration
# --------------------------------------------------
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    # --------------------------------------------------
    # FORMATTERS
    # --------------------------------------------------
    "formatters": {
        "standard": {
            "format": (
                "%(asctime)s | %(levelname)s | %(name)s | "
                "%(filename)s:%(lineno)d | %(message)s"
            )
        }
    },

    # --------------------------------------------------
    # HANDLERS
    # --------------------------------------------------
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": LOG_FILE,
        },
    },

    # --------------------------------------------------
    # NAMED LOGGER
    # --------------------------------------------------
    "loggers": {
        "HGNCapp": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False
        },
    },

    # --------------------------------------------------
    # ROOT LOGGER
    # --------------------------------------------------
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    }
}

# Setup data directory path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Setup source data file
SOURCE_FILE = os.path.join(DATA_DIR, f"hgnc_complete_set.txt")

# Setup lightweight data file
DATA_FILE = os.path.join(DATA_DIR, f"lightweight_dataset.json")