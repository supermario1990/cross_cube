#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Blueprint
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import CONFIG
from flask_migrate import Migrate

migrate = Migrate()
mail = Mail()
db = SQLAlchemy()

version = {"major": 0, "minor": 0, "patch": 1}


def get_version():
    return '.'.join(map(str, version.values()))


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
    migrate.init_app(app, db)

    from .olap import olap
    app.register_blueprint(olap, config=current_config, url_prefix='/olap')

    return app
