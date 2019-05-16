from pydrill.client import PyDrill
from pydrill.transport import Transport
from pydrill.client.result import ResultQuery, Result
from pydrill.exceptions import ImproperlyConfigured, ConnectionError, ConnectionTimeout, TransportError

import os
from urllib.parse import urlencode


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


def drill_get(sql):

    if not drill.is_active():
        raise ImproperlyConfigured('Please run Drill first')

    yelp_reviews = drill.query(sql)
    return yelp_reviews.rows


def drill_storage():

    if not drill.is_active():
        raise ImproperlyConfigured('Please run Drill first')

    storage = drill.storage()
    return storage.data


def drill_storage_detail(name):

    if not drill.is_active():
        raise ImproperlyConfigured('Please run Drill first')

    storage = drill.storage_detail(name)
    return storage.data


def drill_storage_enable(name, value=True):

    if not drill.is_active():
        raise ImproperlyConfigured('Please run Drill first')

    storage = drill.storage_enable(name, value)
    return storage.data


def drill_storage_update(name, config):

    if not drill.is_active():
        raise ImproperlyConfigured('Please run Drill first')

    storage = drill.storage_create(name, config)
    return storage.data


def drill_storage_delete(name):

    if not drill.is_active():
        raise ImproperlyConfigured('Please run Drill first')

    storage = drill.storage_delete(name)
    return storage.data
