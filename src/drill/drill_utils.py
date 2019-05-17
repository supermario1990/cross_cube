from pydrill.client import PyDrill
from pydrill.transport import Transport
from pydrill.client.result import ResultQuery, Result
from pydrill.exceptions import ImproperlyConfigured, ConnectionError, ConnectionTimeout, TransportError, QueryError

import os
from urllib.parse import urlencode
from .drill_dbconfig import get_support_drill_config, UnsupportedDBTypeError, DatasourceConfigError


class PyTransport(Transport):

    def perform_request_form_urlencoded(self, method, url, params=None, body=None, headers=None):

        if headers is None:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        if body is not None:
            body = urlencode(body)

            # some clients or environments don't support sending GET with body
            if method in ('HEAD', 'GET') and self.send_get_body_as != 'GET':
                # send it as post instead
                if self.send_get_body_as == 'POST':
                    method = 'POST'

                # or as source parameter
                elif self.send_get_body_as == 'source':
                    if params is None:
                        params = {}
                    params['source'] = body
                    body = None

        if body is not None:
            try:
                body = body.encode('utf-8')
            except (UnicodeDecodeError, AttributeError):
                # bytes/str - no need to re-encode
                pass

        ignore = ()
        timeout = None
        if params:
            timeout = params.pop('request_timeout', None)
            ignore = params.pop('ignore', ())
            if isinstance(ignore, int):
                ignore = (ignore,)

        for attempt in range(self.max_retries + 1):
            connection = self.get_connection()

            try:
                response, data, duration = connection.perform_request(method,
                                                                      url,
                                                                      params,
                                                                      body,
                                                                      ignore=ignore,
                                                                      timeout=timeout,
                                                                      headers=headers)
            except TransportError as e:
                retry = False
                if isinstance(e, ConnectionTimeout):
                    retry = self.retry_on_timeout
                elif isinstance(e, ConnectionError):
                    retry = True
                elif e.status_code in self.retry_on_status:
                    retry = True

                if retry:
                    if attempt == self.max_retries:
                        raise
                else:
                    raise
            else:
                if data:
                    data = self.deserializer.loads(
                        data, mimetype=response.headers.get('Content-Type'))
                else:
                    data = {}
                return response, data, duration


class PyDrillClient(PyDrill):

    def perform_request_form_urlencoded(self, method, url, params=None, body=None, headers=None):
        return self.transport.perform_request_form_urlencoded(method, url, params, body, headers)

    def storage_create(self, name, config, timeout=10):
        result = Result(*self.perform_request_form_urlencoded(**{
            'method': 'POST',
            'url': '/storage/create_update',
            'body': {'name': name, 'config': config},
            'params': {
                'request_timeout': timeout
            },
            'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
        }))
        return result

    # 重写drill.query 加入 autoLimit
    def query_limit(self, sql, limit = 1000, timeout=10):
        """
                Submit a query with limit and return results.

                :param sql: string
                :param timeout: int
                :return: pydrill.client.ResultQuery
                """
        if not sql:
            raise QueryError('No query passed to drill.')

        result = ResultQuery(*self.perform_request(**{
            'method': 'POST',
            'url': '/query.json',
            'body': {
                "queryType": "SQL",
                "query": sql,
                "autoLimit": limit
            },
            'params': {
                'request_timeout': timeout
            }
        }))

        return result


try:
    from config import Config
    current_config = Config[os.getenv('KROS_CONFIG') or 'default']
    drill = PyDrillClient(host=current_config.DRILL_IP,
                          port=current_config.DRILL_PORT,
                          trasport_class=PyTransport)
except Exception as exception:
    drill = PyDrillClient(host="localhost",
                          port=8047,
                          trasport_class=PyTransport)


class DrillException(ImproperlyConfigured):
    """改掉连不上Drill的提示信息"""

    def __str__(self):
        return repr('config error or bi server status error...')

def drill_get(sql, limit=1000):

    if not drill.is_active():
        raise DrillException()

    yelp_reviews = drill.query_limit(sql, limit)
    return yelp_reviews.rows


def drill_storage_update(type, name, config):

    if not drill.is_active():
        raise DrillException()

    drill_config = get_support_drill_config(type)
    if drill_config is None:
        raise UnsupportedDBTypeError()

    if not drill_config.check_config(config):
        raise DatasourceConfigError()

    storage = drill.storage_create(name, config)
    return storage.data


def drill_storage_delete(name):

    if not drill.is_active():
        raise DrillException()

    storage = drill.storage_delete(name)
    return storage.data


def drill_test_dbstatus(type, name, config, test_sql):
    return True


def drill_get_database_by_name(name):
    """查询所有的数据库schema信息"""
    query_sql = "select * from information_schema.schemata where schema_name like '{}%'".format(
        name)
    return drill_get(query_sql)


def drill_get_tablelist_by_database(name, config):
    """
    根据数据源名称.数据库名称查询所有的表信息
    [
        {
            "TABLE_CATALOG": "DRILL",
            "TABLE_NAME": "datasource",
            "TABLE_SCHEMA": "mysql_250.kros",
            "TABLE_TYPE": "TABLE"
        }
    ]
    """
    db_name = config['db_name']
    table_schema = "{}.{}".format(name, db_name)
    query_sql = "SELECT * FROM INFORMATION_SCHEMA.`TABLES` WHERE TABLE_SCHEMA = '{}' ORDER BY TABLE_NAME DESC".format(table_schema)
    data = drill_get(query_sql)
    keys = ['TABLE_NAME', 'TABLE_SCHEMA', 'TABLE_TYPE']
    result = []
    for item in data:
        result.append({ key:value for key,value in item.items() if key in keys })
    return result


def drill_get_table_info(name, config, table_name):
    """查询表的结构信息"""
    db_name = config['db_name']
    table_schema = "{}.{}".format(name, db_name)
    query_sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'".format(table_schema, table_name)
    return drill_get(query_sql)
