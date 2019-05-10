#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
from logging import getLogger, Formatter, StreamHandler, FileHandler

__all__ = [
    "get_logger",
    "create_logger",
]

DEFAULT_LOGGER_PATH = "log"
DEFAULT_LOGGER_NAME = "kolap"
DEFAULT_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logger = None


def get_logger(name=DEFAULT_LOGGER_NAME, path=DEFAULT_LOGGER_PATH, _format=DEFAULT_FORMAT):
    '''
    @description: Get default logger
    @return: 
    '''
    global logger

    if logger:
        return logger
    else:
        return create_logger(name, path, _format)


def create_logger(name=None, path=None, _format=None):
    '''
    @description: Create a default logger
    @return: 
    '''
    global logger
    logger_name = name or DEFAULT_LOGGER_NAME
    logger = getLogger(logger_name)
    logger.propagate = False

    if not logger.handlers:
        formatter = Formatter(fmt=_format or DEFAULT_FORMAT)

        if path:
            if not os.path.exists(path):
                os.makedirs(path)
            handler = FileHandler(path + "/" + logger_name + ".log")
        else:
            handler = StreamHandler()

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
