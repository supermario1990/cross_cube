#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import L, get_logger
from server import create_app, get_version
import os
from db import db_base
from flask import url_for, redirect

print(L("Hello world!"))
app = create_app(os.getenv('KROS_CONFIG') or 'default')
print(app.url_map)

@app.route('/')
@app.route('/index')
def index():
    return  redirect('/olap/')

@app.route('/version')
def version():
    return get_version()
#app.run()
