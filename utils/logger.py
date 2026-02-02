#!/usr/bin/env python3

import logging
import sys
from datetime import datetime

class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",     
        "INFO": "\033[32m",      
        "WARNING": "\033[33m",   
        "ERROR": "\033[31m",    
        "CRITICAL": "\033[41m", 
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        self.logger = logging.getLogger("app")
        self.logger.setLevel(logging.DEBUG)

        if self.logger.handlers:
            return

        handler = logging.StreamHandler(sys.stdout)
        formatter = ColorFormatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def get_logger(self) -> logging.Logger:
        return self.logger


if __name__ == '__main__':
    logger = Logger().get_logger()
    logger.info('Hello from logger!')