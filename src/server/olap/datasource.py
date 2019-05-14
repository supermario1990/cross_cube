#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..decorator import log_request
from . import olap
from db import *
from utils import formatted_response


@olap.route('/datasource', methods=['GET'])
@log_request
def GetAllDatasourceList():
    return formatted_response(Query_Datasource())


@olap.route('/datasource/{datasource_id}', methods=['GET'])
def get_datasource_by_id():
    pass


@olap.route('/datasource', methods=['POST'])
def new_datasource():
    pass


@olap.route('/datasource', methods=['PUT'])
def update_datasource():
    pass


@olap.route('/datasource', methods=['DELETE'])
def delete_datasource():
    pass


@olap.route('/datasource/test/{datasource_id}', methods=['POST'])
def test_datasource():
    pass


@olap.route('/datasource/table_list/{datasource_id}', methods=['POST'])
def query_datasource_table_list():
    pass
