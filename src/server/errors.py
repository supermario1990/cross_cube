# -*- coding: utf-8 -*-

from werkzeug.exceptions import HTTPException
import json


class ServerError(HTTPException):
    code = 500
    error_type = "internal server error"

    def __init__(self, message=None, exception=None, **details):
        super(ServerError, self).__init__()
        self.message = message
        self.exception = exception
        self.details = details

    def get_body(self, environ):
        error = {
            "message": self.message,
            "type": self.__class__.error_type
        }

        if self.exception:
            error["reason"] = str(self.exception)

        if self.details:
            error.update(self.details)

        string = json.dumps({"error": error}, indent=4)
        return string

    def get_headers(self, environ):
        return [('Content-Type', 'application/json')]


class RequestError(ServerError):
    code = 400
    error_type = "bad request"


class NotAuthenticatedError(ServerError):
    code = 401
    error_type = "not authenticated"

    def __init__(self, message=None, exception=None, realm=None, **details):
        super(NotAuthenticatedError, self).__init__(
            message, exception, **details)
        self.message = message
        self.exception = exception
        self.details = details
        self.realm = realm or "Input username and password"

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

    def __init__(self, message=None):
        super(NotFoundError, self).__init__(message)


class ObjectNotFoundError(ServerError):
    code = 404
    error_type = "object not found"

    def __init__(self, obj, objtype=None, message=None):
        super(ObjectNotFoundError, self).__init__(message)
        self.details = {"object": obj}

        if objtype:
            self.details["object_type"] = objtype

        if message:
            self.message = message
        else:
            self.message = "Object '%s' of type '%s' was not found" % (
                obj, objtype)


class ConflictError(ServerError):
    code = 409
    error_type = "resource conflict"
