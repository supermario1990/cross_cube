#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Blueprint
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import CONFIG

mail = Mail()
db = SQLAlchemy()


def create_app(config_name):
    """
    Create and init flask app by config_name
    """

    current_config = CONFIG[config_name]
    app = Flask(__name__)
    app.config.from_object(current_config)
    current_config.init_app(app)

    mail.init_app(app)
    db.init_app(app)

    from .olap import olap
    app.register_blueprint(olap, url_prefix='/olap')

    return app
