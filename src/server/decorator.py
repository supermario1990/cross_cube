#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decorator import decorator
from utils import get_logger
from flask import request, g


@decorator
def log_request(func, *args, **kw):
    if "lang" not in request.args:
        g.locale = None
    else:
        g.locale = request.args.get("lang")

    logger = get_logger()
    logger.debug(request.args)
    result = func(*args, **kw)
    return result
