#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import Flask
from .web.api import api_bp
from .web.admin import admin_bp


def create_app(test_config=None):
    """
    创建和配置app
    :param test_config:
    :return:
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='1234567890abcdef',
        DEBUG=True,
        # SQLALCHEMY_DATABASE_URI=sql_uri
    )

    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    return app
