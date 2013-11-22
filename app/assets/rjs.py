# -*- coding: utf-8 -*-

from ntpath import basename, dirname
from webassets.filter import ExternalTool

__all__ = ('RJS',)


class RJS(ExternalTool):
    """Uses r.js from `RequireJS <http://requirejs.org/>`_ to optimize JavaScript files.

    This filter depends on the NodeJS modules require.js and r.js, installable via npm.
    It takes a JavaScript file and combines it and its defined dependencies into a single
    optimized file (`<http://requirejs.org/docs/optimization.html#onejs/>`_)::

        Bundle('main.js', filters='rjs', 'main.min.js')

    .. warning::
        This filter requires a version of r.js that allows redirecting output to stdout
        with the option ``out=stdout``.

    .. note::
        The only input file for this filter must be the main JavaScript file of your
        require.js based module. That file will also be used as the ``mainConfigFile`` by r.js.

    *Supported configuration options*:

    RJS_BIN (rjs_bin)
        Path to the r.js executable used to compile source files. By default,
        the filter will attempt to run ``r.js`` via the system path.

    NODE_BIN (node_bin)
        Path to the node executable. By default, the filter will attempt to
        use the system installation of node.

    RJS_EXTRA_ARGS (extra_args)
        A list of additional arguments for r.js. See
        `<http://github.com/jrburke/r.js/blob/master/build/example.build.js/>`_ for
        a complete list of options.
    """
    name = 'rjs'
    options = {
        'rjs_bin': 'RJS_BIN',
        'node_bin': 'NODE_BIN',
        'extra_args': 'RJS_EXTRA_ARGS',
    }
    max_debug_level = None

    def open(self, out, source_path, **kw):
        if self.rjs_bin:
            args = [self.node_bin or 'node', self.rjs_bin]
        else:
            args = ['r.js']

        args += ['-o',
                 'mainConfigFile=%s' % source_path,
                 'baseUrl=%s' % dirname(source_path),
                 'name=%s' % basename(source_path).rsplit('.', 1)[0],
                 'out=stdout',
                 'logLevel=4']

        if self.extra_args:
            args.extend(self.extra_args)

        self.subprocess(args, out)
