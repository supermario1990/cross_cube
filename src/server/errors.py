# -*- coding: utf-8 -*-

from werkzeug.exceptions import HTTPException
import json
from flask import Response
from enum import Enum, unique
from utils import formatted_response


@unique
class ErrorCode(Enum):
    QUERY_DATASOURCE_FAILED = 10000
    DELETE_DATASOURCE_FAILED = 10001
    ADD_DATASOURCE_FAILED = 10002
    CONNECT_DRILL_SERVER_FAILED = 10003
    ADD_DATASOURCE_CONFIG_FAILED = 10004
    UNSUPPORTED_DATASOURCE_TYPE = 10005
    UPDATE_DATASOURCE_FAILED = 10006
    TEST_DATASOURCE_FAILED = 10007
    GET_DATASOURCE_TABLES_FAILED = 10008


class ServerError(HTTPException):
    code = 500
    error_type = "internal server error"

    def __init__(self, message=None, exception=None, error_code=None, **details):
        super(ServerError, self).__init__()
        self.message = message
        self.exception = exception
        self.details = details
        self.error_code = error_code
        if error_code is not None:
            if isinstance(error_code, ErrorCode):
                self.error_code = error_code.value

    def get_headers(self, environ):
        return [('Content-Type', 'application/json')]

    def get_body(self, environ):
        status = {
            "type": self.__class__.error_type,
            "message": self.message,
            "error": True,
            "error_code": self.error_code or self.__class__.code,
        }

        if self.exception:
            status["reason"] = str(self.exception)

        if self.details:
            status.update(self.details)

        string = json.dumps({"status": status}, indent=4)
        return string


class RequestError(ServerError):
    code = 400
    error_type = "bad request"


class NotAuthenticatedError(ServerError):
    code = 401
    error_type = "not authenticated"

    def __init__(self, message=None, exception=None, realm=None, error_code=None, **details):
        super(NotAuthenticatedError, self).__init__(
            message, exception, error_code, **details)
        self.realm = realm or "input username and password"

    def get_headers(self, environ):
        headers = super(NotAuthenticatedError, self).get_headers(environ)
        headers.append(('WWW-Authenticate', 'Basic realm="%s"' % self.realm))
        return headers


class NotAuthorizedError(ServerError):
    code = 403
    error_type = "not authorized"


class NotFoundError(ServerError):
    code = 404
    error_type = "not found"


class ObjectNotFoundError(ServerError):
    code = 404
    error_type = "object not found"

    def __init__(self, obj, objtype=None, message=None, exception=None, error_code=None, **details):
        super(ObjectNotFoundError, self).__init__(
            message, exception, error_code, details)
        self.details = {"object": obj}

        if objtype:
            self.details["object_type"] = objtype

        if message:
            self.message = message
        else:
            self.message = "Object '{}' of type '{}}' was not found".format(
                obj, objtype)


class ConflictError(ServerError):
    code = 409
    error_type = "resource conflict"


class CommonException(ServerError):
    code = 200
    error_type = "request exception"


class CommonFailed:

    def __init__(self, message=None, error_code=None, result=None, **details):
        self.message = message
        self.result = result
        self.details = details
        self.error_code = error_code
        if error_code is not None:
            if isinstance(error_code, ErrorCode):
                self.error_code = error_code.value

    def Result(self):
        status = {
            "message": self.message,
            "error": True,
            "error_code": self.error_code,
        }

        if self.details:
            status.update(self.details)

        result = {}
        result.update({"status": status})

        if self.result is not None:
            result.update({"result": self.result})

        return formatted_response(result)


class CommonSuccess:

    def __init__(self, message=None, result=None, **details):
        self.message = message
        self.result = result
        self.details = details

    def Result(self):
        status = {
            "message": self.message,
            "error": False,
            "error_code": 0,
        }

        if self.details:
            status.update(self.details)

        result = {}
        result.update({"status": status})

        if self.result is not None:
            result.update({"result": self.result})

        return formatted_response(result)
