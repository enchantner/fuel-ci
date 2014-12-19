# -*- coding: utf-8 -*-

import os

from fuel_ci import utils


def build(package, obj):
    build_command = "python setup.py sdist"
    with utils.cd(obj.package_path):
        utils.execute_cmd(build_command)
    build_path = os.path.join(obj.package_path, "dist")
    for f in os.listdir(build_path):
        if f.endswith(".tar.gz"):
            package.path = os.path.join(build_path, f)
            break
