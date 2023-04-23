import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.DEBUG):
    handler = RotatingFileHandler(log_file + '/log.txt', maxBytes=1000000, backupCount=5)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(module)s - %(message)s')
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

logger = setup_logger('logs/IoTShield.log', 'Clog')
