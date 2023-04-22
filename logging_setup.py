import logging
from logging.handlers import RotatingFileHandler


def get_logger(name, level=logging.DEBUG, log_file='logs/IoTShield.log'):
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(module)s - %(message)s')
    handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
