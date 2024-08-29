import logging.config


class LoggingConfig:
    LOG_FORMAT = "[%(levelname)s] - %(asctime)s - %(name)s: %(message)s"
    LOG_FILENAME = "main_service/data.log"

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
                "level": "INFO",
                "formatter": "simple",
                "filename": LOG_FILENAME,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
            }
        },
    }

    def get_logger(self):
        logging.config.dictConfig(self.LOGGING_CONFIG)
        return logging.getLogger()


logging_config = LoggingConfig()
