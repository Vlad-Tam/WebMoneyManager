import logging.config

LOG_FORMAT = "[%(levelname)s] - %(asctime)s - %(name)s: %(message)s"
LOG_FILENAME = "data.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "simple",
            "filename": LOG_FILENAME,
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()
