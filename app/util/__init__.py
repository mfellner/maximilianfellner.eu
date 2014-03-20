# -*- coding: utf-8 -*-

from os import urandom, path, chmod
from subprocess import Popen, PIPE


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


def get_revision():
    """Returns current git revision."""
    try:
        git = Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=PIPE)
        revision = git.stdout.read()
        git.wait()
        return revision
    except OSError:
        return None
