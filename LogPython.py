import logging
from logzero import logger
from logzero import setup_logger
import logzero
import ctypes

import re
from re import RegexFlag

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) 

logging.basicConfig(level = logging.INFO,
                    format = '{ShGLogger v 1.0} %(asctime)s %(process)-6s %(filename)s {%(levelname)s} : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename = "LogPython_info.log",
                    filemode = 'a')

LOG = logging.getLogger('ShGLogger v 1.1')

log_format = '%(color)s [%(asctime)s - %(threadName)s] [%(filename)s %(process)s] [%(levelname)-7s] %(message)s'                        
formatter = logzero.LogFormatter(fmt=log_format)
logzero.setup_default_logger(formatter=formatter)

class LogManager:

    class info:
        def __init__(self, context):
            self.context = context

            logger.info(self.context)
            LOG.info(self.context)
        
        def __str__(self, context):
            return self.context

    class warning:
        def __init__(self, context):
            self.context = context

            logger.warning(self.context)
            LOG.warning(self.context)

        def __str__(self, context):
            return self.context

    class error:
        def __init__(self, context):
            self.context = context

            logger.error(self.context)
            LOG.error(self.context)
        
        def __str__(self, context):
            return self.context

    class debug:
        def __init__(self, context):
            self.context = context

            logger.debug(self.context)
            LOG.debug(self.context)

        def __str__(self, context):
            return self.context

    class debug_cmd:
        def __init__(self, context):
            self.context = context

            LOG.debug(self.context)

        def __str__(self, context):
            return self.context

    class pre_warn:
        def __init__(self, context):
            print("\033[33m {}" .format(context))

    class get_errors:

        def __init__(self):

            reg = r"\{ERROR\} \: ([^+]+?)\{ShGLogger v 1\.0\}"

            file = open('LogPython_info.log', 'r')

            text = file.read()

            matches = re.findall(reg, text, RegexFlag.MULTILINE)

            completed = []    
   
            for item in matches:
                completed.append(item.replace('{ShGLogger v 1.0}', ''))  

            self.completed = completed

        def __str__(self):
            return str(self.completed[len(self.completed) - 1])                                                 
