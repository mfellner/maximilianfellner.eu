# -*- coding: utf-8 -*-

from os import urandom, path, chmod
from subprocess import Popen, PIPE
import re

from lxml import etree
from flask.ext.script import Command


def read_config(config_file):
    """
    Simply loads the lines of a textfile into a list. Lines starting with '#'
    are ignored. Leading and trailing whitespace is stripped. Useful for
    reading commandline arguments from a file.

    :param config_file: path to the configuration file.
    :type config_file: str

    """
    lst = []
    with open(config_file) as f:
        for line in f.readlines():
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            else:
                lst.append(s)
    return lst


def get_secret(secret_file):
    """
    Returns key from the 'secret' file. Creates a new file if necessary.

    :param secret_file: path to the 'secret' file.
    :type secret_file: str

    """
    if not path.isfile(secret_file):
        with open(secret_file, 'w') as f:
            secret = urandom(24)
            f.write(secret)
            chmod(secret_file, 0o400)
            return secret

    with open(secret_file, 'r') as f:
        return f.read()


def get_revision(short=False):
    """Returns current git revision."""
    try:
        args = ['git', 'rev-parse', 'HEAD']
        if short:
            args.insert(2, '--short')
        git = Popen(args, stdout=PIPE)
        revision = git.stdout.read().strip()
        git.wait()
        return revision
    except OSError:
        return None


def get_angular_routes(folder, routes_file=path.join('js', 'build', 'app.js')):
    """Parse and yield route URLs from AngularJS frontend."""
    pattern = re.compile(r"\s+\$routeProvider\.when\('(/.+)'")

    with open(path.join(folder, routes_file)) as f:
        for line in f:
            m = pattern.match(line)
            if m is not None:
                yield m.groups()[0]


def generate_sitemap(folder, base_url='maximilianfellner.eu', change_freq='daily'):
    """Generate XML sitemap from static frontend."""
    urlset = etree.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')

    for route in get_angular_routes(folder):
        url = etree.SubElement(urlset, 'url')
        loc = etree.SubElement(url, 'loc')
        loc.text = 'http://%s/#!%s' % (base_url, route)
        changefreq = etree.SubElement(url, 'changefreq')
        changefreq.text = change_freq
        priority = etree.SubElement(url, 'priority')
        priority.text = '1.0'

    return etree.tostring(urlset, encoding='utf-8', pretty_print=True)


class GenerateSitemap(Command):
    """Generate XML sitemap."""

    def __init__(self, folder):
        self.folder = folder

    def run(self):
        sitemap = generate_sitemap(self.folder)
        file_path = path.join(self.folder, 'sitemap.xml')
        with open(file_path, 'w') as f:
            f.write(sitemap)
            print('Generated %s' % file_path)
