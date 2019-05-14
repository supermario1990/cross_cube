#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, g, request
from utils import str_to_bool

olap = Blueprint('olap', __name__)


@olap.before_request
def process_common_parameters():
    '''
    @description: 请求前先设置一些参数信息。
    @return: 
    '''

    g.json_record_limit = 1024

    if "prettyprint" in request.args:
        g.prettyprint = str_to_bool(request.args.get("prettyprint"))
    else:
        g.prettyprint = 4


try:
    from .datasource import *
except Exception as exception:
    print(exception)
