import logging
from logging import INFO, error
from sys import prefix
import ctypes

import re
from re import RegexFlag
import datetime
import os

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
    def prefix(level):
        return f"[{datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}] [{__name__} {os.getpid()}] [{level}]"

    class info:                         
        def __init__(self, context):
            self.context = context

            level = "INFO   "

            print(f"\033[32m {LogManager.prefix(level)} {self.context}\033[0m")
            
            try:
                LOG.info(self.context)
            except UnicodeEncodeError:         
                print('--- Logging warning --- >> UnicodeEncodeError')

    class warning:
        def __init__(self, context):
            self.context = context

            level = 'WARNING'

            print(f"\033[33m {LogManager.prefix(level)} {self.context}\033[0m")

            try:
                LOG.info(self.context)
            except UnicodeEncodeError:
                print('--- Logging warning --- >> UnicodeEncodeError')

    class error:
        def __init__(self, context):
            self.context = context

            level = 'ERROR  '

            print(f"\033[31m {LogManager.prefix(level)} {self.context}\033[0m")

            try:
                LOG.error(self.context)
            except UnicodeEncodeError:
                print('--- Logging warning --- >> UnicodeEncodeError')

    class debug:
        def __init__(self, context):
            self.context = context

            level = 'DEBUG  '

            print(f"\033[36m {LogManager.prefix(level)} {self.context}\033[0m")

            try:
                LOG.debug(self.context)
            except UnicodeEncodeError:
                print('--- Logging warning --- >> UnicodeEncodeError')

    class debug_cmd:
        def __init__(self, context):
            self.context = context

            try:
                LOG.debug(self.context)
            except UnicodeEncodeError:
                print('--- Logging warning --- >> UnicodeEncodeError')

    class error_cmd:
        def __init__(self, context):
            self.context = context

            try:
                LOG.error(self.context)
            except UnicodeEncodeError:
                print('--- Logging warning --- >> UnicodeEncodeError')

    class pre_warn:
        def __init__(self, context):
            self.context = context
            
            print("\033[33m {}" .format(self.context))

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
