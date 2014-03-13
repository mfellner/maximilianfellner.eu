# -*- coding: utf-8 -*-

from os import path, pardir, walk, urandom
import fnmatch

from flask.ext.assets import Bundle
from flask.ext.assets import Environment
from webassets.filter import register_filter

from app.assets.rjs import RJS
from app.util import load_config


assets_env = None


def create_environment(app, include_dependencies=True, auto_build=True):
    """Create and configure webassets."""
    assets_env = Environment(app)
    assets_env.auto_build = auto_build
    # We need a r.js version which supports stdout (https://github.com/jrburke/r.js/pull/620).
    assets_env.config['RJS_BIN'] = path.join(app.config['STATIC_ROOT'], 'js', 'vendor', 'r.js')
    assets_env.config['RJS_EXTRA_ARGS'] = load_config(path.join(app.config['DATA_ROOT'], 'r.js.conf'))
    register_filter(RJS)

    # 'less' requires lessc and node.js.
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

    # Hack: disable dependencies to enable the cache (this is a webassets issue).
    if not include_dependencies:
        css_layout.depends = []
        css_errors.depends = []
        js_rjs.depends = []

    assets_env.register('css_layout', css_layout)
    assets_env.register('css_errors', css_errors)
    assets_env.register('js_rjs', js_rjs)


def files(directory, pattern):
    """Return file paths matching the pattern."""
    result = []
    for root, dirnames, filenames in walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            result += path.join(root, filename)
    return result
