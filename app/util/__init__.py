# -*- coding: utf-8 -*-


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
