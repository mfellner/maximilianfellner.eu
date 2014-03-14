# -*- coding: utf-8 -*-

from os import urandom, path


def load_config(config_file):
    """Read the lines of a file into a list.

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


def get_secret(name):
    """Returns secret from file.
    Creates a new secret if necessary."""
    if not path.isfile(name):
        with open(name, 'w') as f:
            secret = urandom(24)
            f.write(secret)
            return secret

    with open(name, 'r') as f:
        return f.read()
