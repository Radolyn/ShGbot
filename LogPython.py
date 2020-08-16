import logging
from logzero import logger
from logzero import setup_logger
import logzero
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) 

logging.basicConfig(level = logging.INFO,
                    format = '{ShGLogger v 1.0} %(asctime)s %(process)-6s %(filename)s {%(levelname)s} : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename = "LogPython_info.log",
                    filemode = 'a')

LOG = logging.getLogger('ShGLogger v 1.0')

log_format = '%(color)s [%(asctime)s - %(threadName)s] [%(filename)s %(process)s] [%(levelname)-7s] %(message)s'
formatter = logzero.LogFormatter(fmt=log_format)
logzero.setup_default_logger(formatter=formatter)

class LogManager:

    @staticmethod
    def info(ctx):
        LOG.info(ctx)
        logger.info(ctx)

    @staticmethod
    def warning(ctx):
        LOG.warning(ctx)
        logger.warning(ctx)

    @staticmethod
    def error(ctx):
        LOG.error(ctx)
        logger.error(ctx)

    @staticmethod
    def debug(ctx):
        LOG.debug(ctx)
        logger.debug(ctx)





