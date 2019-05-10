#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from types import FunctionType


def get_work_path():
    return os.getcwd()


def set_work_path(path):
    os.chdir(path)
    return os.getcwd()


def dir_path(path, callback):
    try:
        ls = os.listdir(path)
    except Exception as exception:
        print(exception)
    else:
        if isinstance(callback, FunctionType):
            for file in ls:
                callback(path, file)
