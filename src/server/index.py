#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from . import get_version

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='KROS', version=get_version())


@main.route('/version')
def version():
    return get_version()
