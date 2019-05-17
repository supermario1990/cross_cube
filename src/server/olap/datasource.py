#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..decorator import log_request
from ..errors import *
from . import olap
from flask import request, g, jsonify
import json
from db import *
from drill import *
from utils import formatted_response


@olap.route('/datasource/', methods=['GET'])
@log_request
def get_all_datasource():
    """
    获取已经注册的数据源配置信息。
    ---
    tags:
      - 查询所有的数据源信息。
    responses:
      200:
        description: 返回数据源配置信息列。
        schema:
          properties:
            id:
              type: string
              description: 数据源UUID
            name:
              type: string
              description: 数据源名称，名称不能重复。
            type:
              type: string
              description: 数据源类型。
            config:
              type: string
              description: 数据源配置。
            test_sql:
              type: string
              description: 数据源测试SQL。
              default: SELECT 1
            modi_time:
              type: time
              description: 数据源创建时间。
    """
    try:
        all_datasource = Query_Datasource()
        if all_datasource is None:
            all_datasource = []
        return CommonSuccess("查询成功...", all_datasource).Result()
    except Exception as exception:
        logger = g.request_logger
        logger.log("获取所有数据源配置信息异常：{}".format(exception))
        raise CommonException("获取所有数据源配置信息异常...",
                              exception,
                              ErrorCode.QUERY_DATASOURCE_FAILED)


@olap.route('/datasource/<id>/', methods=['GET', 'DELETE'])
@log_request
def get_datasource_by_id(id):
    """
    根据数据源ID获取数据源配置信息。
    根据数据源ID删除数据源配置信息。
    ---
    tags:
      - 查询某个数据源信息。
      - 删除某个数据源信息。
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: 数据源ID
    responses:
      500:
        description: 删除后台服务器数据源配置发生错误。
      404:
        description: 删除数据源没有找到。
      200:
        description: 返回单个数据源配置信息。
        schema:
          properties:
            id:
              type: string
              description: 数据源UUID
            name:
              type: string
              description: 数据源名称，名称不能重复。
            type:
              type: string
              description: 数据源类型。
            config:
              type: string
              description: 数据源配置。
            test_sql:
              type: string
              description: 数据源测试SQL。
              default: SELECT 1
            modi_time:
              type: time
              description: 数据源创建时间。
    """
    # 获取操作
    if request.method == 'GET':
        try:
            datasource = Select_Datasource_By_ID(id)
            return CommonSuccess("查询成功...", datasource).Result()
        except Exception as exception:
            logger = g.request_logger
            logger.log("根据数据源ID获取数据源配置信息异常：{}-{}".format(id, exception))
            raise CommonException("根据数据源ID获取数据源配置信息异常...",
                                  exception,
                                  ErrorCode.QUERY_DATASOURCE_FAILED)

    # 删除操作
    if request.method == 'DELETE':
        try:
            datasource = Select_Datasource_By_ID(id)
        except Exception as exception:
            logger = g.request_logger
            logger.log("根据数据源ID删除数据源配置信息异常：{}-{}".format(id, exception))
            raise NotFoundError("根据数据源ID删除数据源配置信息异常...", exception)

        # TODO 这么写有问题，这只能保证删除Drill的操作失败，不会删除数据库配置，
        # TODO 但是Drill删除后，执行删除数据源库配置异常，会导致Drill服务器上的配置已经删除，但是数据库中还存在对应的数据源配置。
        try:
            Delete_Datasource_By_ID(id, False)
            drill_storage_delete(datasource.name)
            db.session.commit()
            return CommonSuccess("删除数据源{}配置成功...".format(id)).Result()
        except Exception as exception:
            db.session.rollback()
            logger = g.request_logger
            logger.log("删除Drill数据源异常：{}".format(exception))
            raise CommonException("删除数据源配置{}失败，此数据源配置服务器内部可能已经不能再使用!".format(id),
                                  exception,
                                  ErrorCode.DELETE_DATASOURCE_FAILED)


@olap.route('/datasource/', methods=['POST'])
@log_request
def new_datasource():
    """
    新增数据源配置信息。
    ---
    tags:
      - 增加某个数据源信息。
    parameters:
      - name: id
        type: string
        required: true
        description: 数据源ID
      - name: name
        type: string
        required: true
        description: 数据源名称
      - name: type
        type: string
        required: true
        description: 数据源类型
      - name: config
        type: string
        required: true
        description: 数据源配置
      - name: test_sql
        type: string
        description: 数据源测试SQL。
    responses:
      500:
        description: 新增数据源内部错误。
      409:
        description: 新增数据源冲突。
      400:
        description: 请求参数错误，请求的参数值不完整。
      200:
        description: 成功。
        schema:
          properties:
            id:
              type: string
              description: 新的数据源ID
            error:
              type: bool
              description: 发生错误此字段为TRUE
            message:
              type: string
              description: 提示信息
    """
    if request.is_json:
        request_data = request.json
    else:
        request_data = request.form
    try:
        name = request_data["name"]
        type = request_data["type"]
        config = request_data["config"]
        test_sql = request_data.get("test_sql")
        if isinstance(config, str):
            config = json.loads(config)
        if isinstance(config, object):
            str_config = json.dumps(config)
    except KeyError as keyerror:
        raise RequestError("请求参数包含的键值不完整!", keyerror)
    except Exception as exception:
        raise RequestError("请求参数异常!", exception)

    try:
        datasource = Select_Datasource_By_Name(name)
    except Exception as exception:
        pass
    if datasource != None:
        raise ConflictError("数据源名称{}冲突".format(name))

    logger = g.request_logger
    try:
        id = Insert_Datasource(name, type, str_config, test_sql, False)
        drill_storage_update(type, name, config)
        db.session.commit()
        return CommonSuccess("新增数据源成功!", {"id": id}).Result()
    except ImproperlyConfigured as exception:
        db.session.rollback()
        logger.log("后台服务器配置错误或者启动异常: {}".format(exception))
        raise CommonException("后台服务器配置错误或者启动异常!", exception,
                              ErrorCode.CONNECT_DRILL_SERVER_FAILED)
    except DatasourceConfigError as exception:
        db.session.rollback()
        logger.log("请求参数Config设置不正确: {}".format(exception))
        raise CommonException("请求参数Config设置不正确!", exception,
                              ErrorCode.ADD_DATASOURCE_CONFIG_FAILED)
    except UnsupportedDBTypeError as exception:
        db.session.rollback()
        logger.log("不支持的数据源类型: {}".format(exception))
        raise CommonException("不支持的数据源类型!", exception,
                              ErrorCode.UNSUPPORTED_DATASOURCE_TYPE)
    except Exception as exception:
        db.session.rollback()
        logger.log("新增数据源配置异常: {}".format(exception))
        raise CommonException("新增数据源配置异常!", exception,
                              ErrorCode.ADD_DATASOURCE_FAILED)


@olap.route('/datasource/', methods=['PUT'])
def update_datasource():
    """
    新增或者修改数据源配置信息。
    ---
    tags:
      - 增加或者修改某个数据源信息。
    parameters:
      - name: id
        type: string
        required: true
        description: 数据源ID
      - name: name
        type: string
        required: true
        description: 数据源名称
      - name: type
        type: string
        required: true
        description: 数据源类型
      - name: config
        type: string
        required: true
        description: 数据源配置
      - name: test_sql
        type: string
        description: 数据源测试SQL。
    responses:
      500:
        description: 新增或者修改数据源内部错误。
      400:
        description: 请求参数错误，请求的参数值不完整。
      200:
        description: 成功。
        schema:
          properties:
            id:
              type: string
              description: 新的数据源ID
            error:
              type: bool
              description: 发生错误此字段为TRUE
            message:
              type: string
              description: 提示信息
    """
    if request.is_json:
        request_data = request.json
    else:
        request_data = request.form
    try:
        id = request_data["id"]
        name = request_data["name"]
        type = request_data["type"]
        config = request_data["config"]
        test_sql = request_data.get("test_sql")
        if isinstance(config, str):
            config = json.loads(config)
        if isinstance(config, object):
            str_config = json.dumps(config)
    except KeyError as keyerror:
        raise RequestError("请求参数包含的键值不完整!", keyerror)
    except Exception as exception:
        raise RequestError("请求参数异常!", exception)

    logger = g.request_logger
    try:
        datasource = Select_Datasource_By_Name(name)
        Update_Datasource(id, name, type, str_config, test_sql, False)
        drill_storage_update(name, config)
        db.session.commit()
        return CommonSuccess("修改或者新增数据源成功!", {"id": id}).Result()
    except ImproperlyConfigured as exception:
        db.session.rollback()
        logger.log("后台服务器配置错误或者启动异常: {}".format(exception))
        raise CommonException("后台服务器配置错误或者启动异常!", exception,
                              ErrorCode.CONNECT_DRILL_SERVER_FAILED)
    except DatasourceConfigError as exception:
        db.session.rollback()
        logger.log("请求参数Config设置不正确: {}".format(exception))
        raise CommonException("请求参数Config设置不正确!", exception,
                              ErrorCode.ADD_DATASOURCE_CONFIG_FAILED)
    except UnsupportedDBTypeError as exception:
        db.session.rollback()
        logger.log("不支持的数据源类型: {}".format(exception))
        raise CommonException("不支持的数据源类型!", exception,
                              ErrorCode.UNSUPPORTED_DATASOURCE_TYPE)
    except Exception as exception:
        try:
            if datasource is None:
                # 新增数据源配置，执行删除Drill对应的配置。
                drill_storage_delete(name)
                error_code = ErrorCode.ADD_DATASOURCE_FAILED
            else:
                # 修改数据源配置，执行恢复Drill对应的配置。
                drill_storage_update(datasource.name,
                                     json.loads(datasource.config))
                error_code = ErrorCode.UPDATE_DATASOURCE_FAILED
        except Exception as exception:
            pass
        db.session.rollback()
        logger.log("修改或者新增数据源配置异常: {}".format(exception))
        raise CommonException("修改或者新增数据源配置异常!", exception, error_code)


@olap.route('/datasource/test/<datasource_id>', methods=['GET', 'POST'])
def test_datasource():
    pass


@olap.route('/datasource/table_list/<datasource_id>', methods=['GET', 'POST'])
def query_datasource_table_list():
    pass
