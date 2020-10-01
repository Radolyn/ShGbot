import logging
from logging import INFO, error
import ctypes

import re
from re import RegexFlag
import datetime
import os
from sys import stdout
    
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) 

logging.basicConfig(level = logging.INFO,
                    format = '{ShGLogger v 1.0} %(asctime)s %(process)-6s %(filename)s {%(levelname)s} : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename = "LogPython_info.log",
                    filemode = 'a')

LOG = logging.getLogger('ShGLogger v 1.0')

class LogManager:

    @staticmethod
    def prefix(type:str, level:str):
        if type == 'logger_cmd':
            return f"[{datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}] [{__name__} {os.getpid()}] [{level}]"
        else:
            pass
            """Undefined prefix method"""

    def info(self, context):                        
        self.context = context

        level = "INFO   "

        stdout.writelines(f"\033[32m {LogManager.prefix('logger_cmd', level)} {self.context}\033[0m \n")
        
        try:
            LOG.info(self.context)
        except UnicodeEncodeError:         
            stdout.writelines('--- Logging warning --- >> UnicodeEncodeError \n')

    def warning(self, context):
        self.context = context

        level = 'WARNING'

        stdout.writelines(f"\033[33m {LogManager.prefix('logger_cmd', level)} {self.context}\033[0m \n")

        try:
            LOG.info(self.context)
        except UnicodeEncodeError:
            stdout.writelines('--- Logging warning --- >> UnicodeEncodeError \n')

    def error(self, context):
        self.context = context

        level = 'ERROR  '

        stdout.writelines(f"\033[31m {LogManager.prefix('logger_cmd', level)} {self.context}\033[0m \n")

        try:
            LOG.error(self.context)
        except UnicodeEncodeError:
            stdout.writelines('--- Logging warning --- >> UnicodeEncodeError \n')

    def debug(self, context):
        self.context = context

        level = 'DEBUG  '

        stdout.writelines(f"\033[36m {LogManager.prefix('logger_cmd', level)} {self.context}\033[0m \n")

        try:
            LOG.debug(self.context)
        except UnicodeEncodeError:
            stdout.writelines('--- Logging warning --- >> UnicodeEncodeError \n')

    def debug_cmd(self, context):
        self.context = context

        level = 'DEBUG  '

        try:
            LOG.debug(self.context)
        except UnicodeEncodeError:
            stdout.writelines('--- Logging warning --- >> UnicodeEncodeError \n')

    def debug_log(self, context):
        self.context = context

        try:
            LOG.debug(self.context)
        except UnicodeEncodeError:
            stdout.writelines('--- Logging warning --- >> UnicodeEncodeError \n')

    def error_log(self, context):
        self.context = context

        try:
            LOG.error(self.context)
        except UnicodeEncodeError:
            stdout.writelines('--- Logging warning --- >> UnicodeEncodeError \n')

    def info_cmd(self, context):
        level = "INFO   "
        self.context = context

        stdout.writelines(f"\033[32m {LogManager.prefix('logger_cmd', level)} {self.context}\033[0m \n")

    def pre_warn(self, context):
        context = context
            
        stdout.writelines("\033[33m {}" .format(context))

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
