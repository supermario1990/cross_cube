#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Response, request, g
import os
import base64
from types import FunctionType
from .formatters import JSONEncoder


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


def generate_secretkey(key_len=48):
    return base64.b64encode(os.urandom(key_len)).decode()


def str_to_bool(string):
    """Convert a `string` to bool value. Returns ``True`` if `string` is
    one of ``["true", "yes", "1", "on"]``, returns ``False`` if `string` is
    one of  ``["false", "no", "0", "off"]``, otherwise returns ``None``."""

    if string is not None:
        if string.lower() in ["true", "yes", "1", "on"]:
            return True
        elif string.lower() in["false", "no", "0", "off"]:
            return False

    return None


def formatted_response(response):
    """
    返回`application/json, 转换对象到JSON。
    """

    if g.prettyprint:
        indent = 4
    else:
        indent = None

    encoder = JSONEncoder(indent=indent)
    encoder.iterator_limit = g.json_record_limit
    data = encoder.iterencode(response)

    return Response(data, mimetype='application/json')
