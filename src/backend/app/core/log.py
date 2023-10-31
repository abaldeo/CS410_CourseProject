
import logging
from loguru import logger
import inspect
import sys 
from .config import settings

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def configure_logging():
    config = {
        "handlers": [
            {"sink": sys.stdout, 
             "format": "[<green>{time:YYYY-MM-DD HH:mm:ss}</green>][<level>{level}</level>] <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
             "level": "INFO",  "diagnose": False if "prod" in settings.ENVIRONMENT.lower()  else True
             },
            #{"sink": "file.log", "serialize": True, "enqueue": True},
        ],
    }
    logger.configure(**config)
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    logger.info("Configured logging")

