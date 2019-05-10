#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Blueprint
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    mail.init_app(app)
    db.init_app(app)

    from .olap import olap
    app.register_blueprint(olap, url_prefix='/olap')

    return app
