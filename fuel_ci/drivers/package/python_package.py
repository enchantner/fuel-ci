# -*- coding: utf-8 -*-
#    Copyright 2014 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

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
