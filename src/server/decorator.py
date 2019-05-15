#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decorator import decorator
from flask import request, g


@decorator
def log_request(func, *args, **kw):
    logger = g.request_logger
    params = {
        "full_path": request.full_path,
        "url": request.url,
        "script_root": request.script_root,
        "accept_charsets": request.accept_charsets,
        "accept_encodings": request.accept_encodings,
        "accept_languages": request.accept_languages,
        "accept_mimetypes": request.accept_mimetypes,
        "access_route": request.access_route,
        "args": request.args,
        "authorization": request.authorization,
        "cache_control": request.cache_control,
        "content_encoding": request.content_encoding,
        "content_length": request.content_length,
        "content_type": request.content_type,
        "cookies": request.cookies,
        "data": request.data,
        "date": request.date,
        "files": request.files,
        "host": request.host,
        "is_json": request.is_json,
    }
    logger.log(request.method, request.path, params)
    result = func(*args, **kw)
    return result
