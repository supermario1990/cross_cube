#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..decorator import log_request
from . import olap
from flask import request
import json
from db import *
from utils import formatted_response


@olap.route('/datasource', methods=['GET'])
@log_request
def get_all_datasource():
    return formatted_response(Query_Datasource())


@olap.route('/datasource/<datasource_id>', methods=['GET'])
def get_datasource_by_id(datasource_id):
    return formatted_response(Select_Datasource_By_ID(datasource_id))


@olap.route('/datasource', methods=['POST'])
def new_datasource():
    pass


@olap.route('/datasource', methods=['PUT'])
def update_datasource():
    pass


@olap.route('/datasource', methods=['DELETE'])
def delete_datasource():
    pass


@olap.route('/datasource/test/<datasource_id>', methods=['GET', 'POST'])
def test_datasource():
    pass


@olap.route('/datasource/table_list/<datasource_id>', methods=['GET', 'POST'])
def query_datasource_table_list():
    pass
