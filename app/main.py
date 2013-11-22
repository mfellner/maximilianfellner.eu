# -*- coding: utf-8 -*-

import re
import time
import fnmatch
from os import path, pardir, walk, urandom

from flask import Flask
from flask.ext.assets import Bundle
from flask.ext.assets import Environment
from webassets.filter import register_filter

from app.util import load_config
from app.assets.rjs import RJS
from app.shared.models import db
from app.shared.api import shared_bp, get_root_index
from app.blog.api import blog_bp
from app.admin.api import admin_bp


APPLICATION_ROOT = path.dirname(path.abspath(path.join(__file__, pardir)))
DATA_ROOT = path.join(APPLICATION_ROOT, 'data')
STATIC_ROOT = path.join(APPLICATION_ROOT, 'static')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(DATA_ROOT, 'main.db')
SECRET_KEY = urandom(24)

# Configuration for r.js webassets filter.
RJS_BIN = path.join(STATIC_ROOT, 'js', 'vendor', 'r.js')
RJS_EXTRA_ARGS = load_config(path.join(DATA_ROOT, 'r.js.conf'))


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

    # Configure webassets.
    assets = Environment(app)
    register_filter(RJS)

    css_layout = Bundle(path.join('css', 'less', 'layout.less'),
                        output=path.join('css', 'layout.min.css'),
                        filters='less, cssmin',
                        depends=files(path.join(app.static_folder, 'css', 'less'), '*.less'))

    css_errors = Bundle(path.join('css', 'less', 'errors.less'),
                        output=path.join('css', 'errors.min.css'),
                        filters='less, cssmin')

    js_rjs = Bundle(path.join('js', 'build', 'main.js'),
                    output=path.join('js', 'main.min.js'),
                    filters='rjs',
                    depends=files(path.join(app.static_folder, 'js', 'build'), '*.js'))

    # Hack: enable cache by disabling dependencies in production (this is a webassets issue).
    if not debug:
        css_layout.depends = []
        css_errors.depends = []
        js_rjs.depends = []

    assets.register('css_layout', css_layout)
    assets.register('css_errors', css_errors)
    assets.register('js_rjs', js_rjs)

    # Initialize SQLAlchemy connection with the application.
    db.init_app(app)

    # Add a Jinja context processor.
    app.context_processor(current_year)

    return app


def register_frontend_routes(app):
    """Hack: add URL rules for all routes configured in the
    AngularJS frontend using Flask's pluggable views."""
    angular_routes = path.join(app.static_folder, 'js', 'build', 'app.js')

    p = re.compile("\s+\$routeProvider\.when\('(/.+)'")

    with open(angular_routes) as f:
        for line in f:
            m = p.match(line)
            if m is not None:
                route = m.groups()[0]
                app.add_url_rule(route, view_func=get_root_index)


def current_year():
    """Function for template context processor returning the current year."""
    return dict(current_year=time.strftime('%Y'))


def files(directory, pattern):
    """Yield files matching the pattern."""
    result = []
    for root, dirnames, filenames in walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            result += path.join(root, filename)
    return result
