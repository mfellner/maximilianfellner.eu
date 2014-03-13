# -*- coding: utf-8 -*-

import re
import time
from os import path, pardir, urandom

from flask import Flask

from app.assets import create_environment
from app.shared.models import db
from app.shared.api import shared_bp, get_root_index
from app.blog.api import blog_bp
from app.admin.api import admin_bp


APPLICATION_ROOT = path.dirname(path.abspath(path.join(__file__, pardir)))
DATA_ROOT = path.join(APPLICATION_ROOT, 'data')
STATIC_ROOT = path.join(APPLICATION_ROOT, 'static')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(DATA_ROOT, 'main.db')
SECRET_KEY = urandom(24)


def create_app(debug=False):
    app = Flask(__name__.split('.')[0],
                static_folder=STATIC_ROOT,
                template_folder=path.join(APPLICATION_ROOT, 'templates'))

    app.config.from_object(__name__)
    app.debug = debug

    app.register_blueprint(shared_bp)
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    register_frontend_routes(app)

    # Configure webassets environment.
    create_environment(app, debug, debug)

    # Initialize SQLAlchemy connection with the application.
    db.init_app(app)

    # Add a Jinja context processor.
    app.context_processor(current_year)

    return app


def register_frontend_routes(app):
    """Hack: add URL rules for all routes configured in the
    AngularJS frontend using Flask's pluggable views."""
    angular_routes = path.join(app.static_folder, 'js', 'build', 'app.js')

    p = re.compile(r"\s+\$routeProvider\.when\('(/.+)'")

    with open(angular_routes) as f:
        for line in f:
            m = p.match(line)
            if m is not None:
                route = m.groups()[0]
                app.add_url_rule(route, view_func=get_root_index)


def current_year():
    """Function for template context processor returning the current year."""
    return dict(current_year=time.strftime('%Y'))
