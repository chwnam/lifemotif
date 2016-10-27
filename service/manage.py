#!/usr/bin/env python
import os
import sys
import re

var_expr = re.compile(r'^export\s+(?P<key>.+?)=(?P<value>.+?)\s*$')


def import_settings(file_path):
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


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")
    import_settings('../service_env')

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
