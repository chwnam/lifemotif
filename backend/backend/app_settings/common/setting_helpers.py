from django.core.exceptions import ImproperlyConfigured
from importlib import import_module

import os
from re import compile as re_compile

var_expr = re_compile(r'^export\s+(?P<key>.+?)=("|\')?(?P<value>.+?)("|\')?\s*$')


def get_env(key, strict=False, default=None):
    """
    get an environment variable value by key.
    :param key: name to look for. Capital characters are preferred.
    :param strict: if it is true and an environment variable is not set, then ImproperlyConfigured exception will occur.
    :param default: when strict is false and an environment variable is not present, this value will be returned.
    :return:
    """
    if strict and key not in os.environ:
        raise ImproperlyConfigured('Key \'{}\' not found in the environment variables'.format(key))
    return os.environ.get(key=key, default=default)


def import_all(package, global_space):
    """
    Behaves just like "from x.y.z import *".
    :param package: use absolute python package path
    :param global_space:
    :return:
    """
    module = import_module(package)
    if module:
        global_space.update({k: v for k, v in module.__dict__.items() if not k.startswith('__')})


def set_env_from_file(file_path):
    """
    Imports classical "export KEY=VALUE" style environment variables.
    Note that this file's content should be simple as it can be.
    Do not use control statement, such as if, for ... this function is not an interpreter!
    :param file_path:
    :return:
    """
    if not os.path.exists(file_path):
        return
    with open(file_path) as f:
        for line in f:
            m = var_expr.match(line)
            if not m:
                continue
            key = m.groupdict().get('key')
            value = m.groupdict().get('value')
            if not key or not value:
                continue
            os.environ.setdefault(key, value)
