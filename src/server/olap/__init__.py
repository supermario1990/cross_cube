#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, g, request
from werkzeug.exceptions import NotFound
from utils import str_to_bool, jsonify, get_logger, CustomDict, GLOBAL_LANG
from ..decorator import log_request
from ..logging import configured_request_log_handlers, RequestLogger, AsyncRequestLogger

olap = Blueprint('olap', __name__)

try:
    from .datasource import *
    from .routes import *
except Exception as exception:
    print(exception)


def storage_attr_ifnotexist(config, attr_name, value):
    has_attr, value = config.has_attr(attr_name)
    if not has_attr:
        setattr(config, attr_name.upper(), value)


@olap.record_once
def initialize_olap(state):
    with state.app.app_context():
        config = state.options["config"]

        logger = get_logger()
        custom_dict = CustomDict()

        current_app.olap = custom_dict
        current_app.olap.config = config

        storage_attr_ifnotexist(config, "ASYNC_LOG", False)
        storage_attr_ifnotexist(config, "LANG", GLOBAL_LANG)
        storage_attr_ifnotexist(config, "PRETTY_PRINT", False)
        storage_attr_ifnotexist(config, "JSON_RECORD_LIMIT", 1024)

        has_attr, value = config.has_attr("LOGGER_OUTPUT_TYPE")
        if has_attr and value:
            handlers = configured_request_log_handlers(
                config.LOGGER_LEVEL, value)

            has_attr, value = config.has_attr("ASYNC_LOG")
            if has_attr and value:
                current_app.olap.request_logger = AsyncRequestLogger(handlers)
            else:
                current_app.olap.request_logger = RequestLogger(handlers)


@olap.before_request
def process_common_parameters():
    g.JSON_RECORD_LIMIT = current_app.olap.config.JSON_RECORD_LIMIT
    g.request_logger = current_app.olap.request_logger

    if "lang" not in request.args:
        g.LOCALE = None
    else:
        g.LOCALE = request.args.get("lang")

    if "prettyprint" not in request.args:
        g.PRETTY_PRINT = False
    else:
        g.PRETTY_PRINT = str_to_bool(request.args.get("prettyprint"))


@olap.errorhandler(NotFound.code)
@log_request
def not_found(e):
    error = {
        "error": "not found",
        "message": "The requested URL was not found on the server."
    }
    return jsonify(error), NotFound.code
