# -*- coding: utf-8 -*-
"""logger

Logger class
"""

import os
import re
import inspect
import traceback
import logging
import logging.handlers

# logging level
LOGGING_LEVEL = logging.DEBUG

# file log settings
_FILE_LOG_DIR = os.getcwd()
_FILE_LOG_MAX_BYTES = 1024 * 1024
_FILE_LOG_BACKUP_COUNT = 2

# formatter
_FILE_LOG_FORMAT = '%(asctime)s,%(levelname)s,%(message)s'
_FILE_LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
_STREAM_LOG_FORMAT = '[%(asctime)s] %(levelname)s %(message)s'
_STREAM_LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class Logger():
    """Logger"""

    def __init__(self, unique_id=None,
                 file_output=False, stream_output=True, trace=False):
        self.trace = trace

        # aquire logger instance
        caller = self.__caller(depth=2)
        name = caller['path']
        if isinstance(unique_id, int):
            name += '_' + str(unique_id)
        self.__logger = logging.getLogger(name)
        self.__logger.propagate = False
        self.__logger.setLevel(LOGGING_LEVEL)

        # clear output handlers
        if self.__logger.handlers:
            self.__logger.handlers.pop()

        # setup file output handler
        if file_output:
            root, _ = os.path.splitext(os.path.basename(caller['path']))
            root = re.sub(re.compile("[[]{}<>]"), "", root)
            path = os.path.join(_FILE_LOG_DIR, root + '.log')
            fh = logging.handlers.RotatingFileHandler(filename=path,
                                                      maxBytes=_FILE_LOG_MAX_BYTES,
                                                      backupCount=_FILE_LOG_BACKUP_COUNT)
            formatter = logging.Formatter(_FILE_LOG_FORMAT,
                                          datefmt=_FILE_LOG_DATE_FORMAT)
            fh.setFormatter(formatter)
            self.__logger.addHandler(fh)

        # setup stream output handler
        if stream_output:
            sh = logging.StreamHandler()
            formatter = logging.Formatter(_STREAM_LOG_FORMAT,
                                          datefmt=_STREAM_LOG_DATE_FORMAT)
            sh.setFormatter(formatter)
            self.__logger.addHandler(sh)

    def critical(self, fmt, *args, **kwargs):
        """critical message"""
        self.__logger.critical(self.__fmt(fmt), *args, **kwargs)
        self.__logger.critical(traceback.format_exc())

    def error(self, fmt, *args, **kwargs):
        """error message"""
        self.__logger.error(self.__fmt(fmt), *args, **kwargs)

    def info(self, fmt, *args, **kwargs):
        """info message"""
        self.__logger.info(self.__fmt(fmt), *args, **kwargs)

    def debug(self, fmt, *args, **kwargs):
        """debug message"""
        self.__logger.debug(self.__fmt(fmt), *args, **kwargs)

    def process_start(self):
        """process start message"""
        self.info('start')

    def process_end(self, status_code=0, system_exit=False):
        """process end message"""
        func = self.info if status_code == 0 else self.critical
        message = 'end (SystemExit)' if system_exit else 'end'
        func(message)

    def __fmt(self, fmt):
        if self.trace:
            caller = self.__caller(depth=3)
            fmt += " ({}:{}:{})".format(os.path.basename(caller['path']),
                                        caller['lineno'], caller['function'])
        return fmt

    def __caller(self, depth=1):
        stack = inspect.stack()[depth]
        return {
            'path': os.path.abspath(stack.filename),
            'lineno': stack.lineno,
            'function': stack.function
        }
