# settings.py
"""
LOGGING CONFIGURATION (DEFENSIVE VERSION)

----------------------------------------
WHAT THIS TEACHES
----------------------------------------
✔ Centralised logging configuration
✔ Safe file handling
✔ Defensive programming
✔ Logger naming conventions (important in real systems)

KEY IDEA:
Even when things seem simple, we still validate inputs
and design logging for clarity, consistency, and extensibility.
"""

import os
from pathlib import Path

# --------------------------------------------------
# STEP 1: Define default log file (hidden, home directory)
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
    # OPTIONAL: NAMED LOGGER (TEACHING EXAMPLE)
    # --------------------------------------------------
    # Why define a named logger?
    # - Gives fine-grained control over specific parts of your app
    # - Lets you tune verbosity per module/package
    #
    # BEST PRACTICE:
    # - Name your logger after your *top-level package*
    #   e.g. package: HGNCapp → logger: "HGNCapp"
    #
    # WHY?
    # - Keeps logs consistent and predictable
    # - Makes filtering/searching easier
    # - Matches how logging.getLogger(__name__) resolves names
    #
    # HOWEVER:
    # You can deliberately override naming if it improves clarity.
    #
    # Example:
    # - Your package is "HGNCapp"
    # - But you want cleaner logs → use "SeqKit"
    #
    # Trade-off:
    # ✔ Cleaner log labels
    # ✖ Slightly less direct mapping to Python module paths
    #


    "loggers": {
        "HGNCapp": {

            # The logging level for this specific logger
            # DEBUG = capture EVERYTHING (lowest threshold)
            # Helps when you want deep visibility into this component
            "level": "DEBUG",

            # Handlers define *where* the logs go:
            # - "console" → terminal/stdout (human-readable, immediate)
            # - "file"    → persistent storage for later analysis
            #
            # Multiple handlers = same message sent to multiple destinations
            "handlers": ["console", "file"],

            # propagate controls whether logs "bubble up" to parent loggers
            #
            # False (recommended here):
            # - prevents duplicate log entries
            # - ensures this logger is self-contained
            # - useful when you explicitly define handlers for this logger
            #
            # True would:
            # - pass logs to parent/root loggers as well
            # - can cause duplicate messages if those loggers use the same handlers
            #
            # NOTE (important in real systems):
            # - This can be intentionally overridden when your code is used as a library
            # - e.g. if HGNCapp is imported into a larger application (CLI, web app)
            #   the parent application may want to control logging centrally
            # - In that case, setting propagate=True allows integration into the host app’s logging

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

# Setup data file
DATA_FILE = os.path.join(DATA_DIR, f"lightweight_dataset.json")