# -*- coding: utf-8 -*-

from contextlib import contextmanager
from threading import Thread
from queue import Queue
from flask import request

import datetime
import time
import json

from utils import get_logger, create_logger, DEFAULT_LOGGER_PATH


class DefaultRequestLogHandler():
    def __init__(self, logger=None, **options):
        self.logger = logger

    def set_level(self, level):
        self.logger.setLevel(level)

    def write_record(self, record, params, **options):
        self.logger.info("Method:{:<7} Path:{:<30} Timestamp:{:<20} Elapsed_time:{:<10} Params:{}"
                         .format(record["method"], record["path"], record["timestamp"], record["elapsed_time"], params))


default_logger_handler = DefaultRequestLogHandler(get_logger())
console_logger_handler = DefaultRequestLogHandler(create_logger("console"))


def configured_request_log_handlers(level, type=["default"]):
    handlers = []
    for item in type:
        if item == "default":
            handlers.append(default_logger_handler)
            default_logger_handler.set_level(level)
        if item == "console":
            handlers.append(console_logger_handler)
            console_logger_handler.set_level(level)
    return handlers


class RequestLogger(object):
    def __init__(self, handlers=None):
        if handlers:
            self.handlers = list(handlers)
        else:
            self.handlers = []

        self.logger = get_logger()

    @contextmanager
    def log_time(self, params, method=None, path=None, **other):
        start = time.time()
        yield
        elapsed = time.time() - start
        self.log(params, method, path, elapsed, **other)

    def log(self, params, method=None, path=None, elapsed=None, **other):
        record = {
            "timestamp": time.time(),
            "method": method or request.method,
            "path": path or request.path,
            "elapsed_time": elapsed or 0,
        }
        record.update(other)

        for handler in self.handlers:
            try:
                handler.write_record(record, params)
            except Exception as e:
                self.logger.error(
                    "Server log handler error (%s): %s" % (type(handler).__name__, str(e)))


class AsyncRequestLogger(RequestLogger):
    def __init__(self, handlers=None):
        super(AsyncRequestLogger, self).__init__(handlers)
        self.queue = Queue()
        self.thread = Thread(target=self.log_consumer, name="logging_thread")
        self.thread.daemon = True
        self.thread.start()

    def log(self, *args, **kwargs):
        self.queue.put((args, kwargs))

    def log_consumer(self):
        while True:
            (args, kwargs) = self.queue.get()
            super(AsyncRequestLogger, self).log(*args, **kwargs)
