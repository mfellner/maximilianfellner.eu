# -*- coding: utf-8 -*-

from os import path, walk
import fnmatch

from flask.ext.assets import Bundle
from flask.ext.assets import Environment
from webassets.filter import register_filter

from app.assets.rjs import RJS
from app.util import read_config


assets_env = Environment()


def init_assets_environment(app, include_dependencies=True, auto_build=True):
    """Configure Flask webassets."""
    # Configuration must be set directly on Flask.config because Environment
    # needs to have a Flask application in the context in order to do that.
    app.config['ASSETS_AUTO_BUILD'] = auto_build
    # We need a r.js version which supports stdout (https://github.com/jrburke/r.js/pull/620).
    app.config['RJS_BIN'] = path.join(app.config['STATIC_ROOT'], 'js', 'vendor', 'r.js')
    app.config['RJS_EXTRA_ARGS'] = read_config(path.join(app.config['DATA_ROOT'], 'r.js.conf'))

    register_filter(RJS)

    # 'less' requires lessc and node.js (see package.json).
    css_layout = Bundle(path.join('css', 'less', 'layout.less'),
                        output=path.join('css', 'layout.min.css'),
                        filters='less, cssmin',
                        depends=files(path.join(app.static_folder, 'css', 'less'), '*.less'))

    css_errors = Bundle(path.join('css', 'less', 'errors.less'),
                        output=path.join('css', 'errors.min.css'),
                        filters='less, cssmin')

    # 'rjs' requires r.js and node.js.
    js_rjs = Bundle(path.join('js', 'build', 'main.js'),
                    output=path.join('js', 'main.min.js'),
                    filters='rjs',
                    depends=files(path.join(app.static_folder, 'js', 'build'), '*.js'))

    # Hack: exclude dependencies in order to enable caching (this is a webassets issue).
    if not include_dependencies:
        css_layout.depends = []
        css_errors.depends = []
        js_rjs.depends = []

    assets_env.register('css_layout', css_layout)
    assets_env.register('css_errors', css_errors)
    assets_env.register('js_rjs', js_rjs)

    assets_env.init_app(app)


def files(directory, pattern):
    """Returns file paths matching the pattern."""
    result = []
    for root, dirnames, filenames in walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            result += path.join(root, filename)
    return result
