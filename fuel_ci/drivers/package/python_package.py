# -*- coding: utf-8 -*-

"""
Driver for building python package from source
"""

import os

from fuel_ci import utils


def build(package, obj):
    """Build installable ".tar.gz" python package.

    :param package: (Package) object
    :param obj: (Repository) object with "package_path" attribute
    """
    build_path = os.path.join(obj.package_path, "dist")
    find_exist = lambda build_path: [
        os.path.join(build_path, f) for f in os.listdir(build_path)
        if f.endswith(".tar.gz")
    ] or None
    exist_path = find_exist(build_path)
    if not exist_path:
        build_command = "python setup.py sdist"
        with utils.cd(obj.package_path):
            utils.execute_cmd(build_command)
    package.path = find_exist(build_path)[0]
