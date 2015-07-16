# -*- coding: utf-8 -*-
"""
    app
    ~~~

    Provides the flask application
"""
from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import config

from os import getenv, path as p
from flask import Flask, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(mode=None):
    # Create webapp instance
    app = Flask(__name__)
    db.init_app(app)

    if mode:
        app.config.from_object(getattr(config, mode))
    else:
        app.config.from_envvar('APP_SETTINGS', silent=True)

    @app.route('/')
    def home():
        return 'Welcome to the UN Habitat API Collector!'

    return app
