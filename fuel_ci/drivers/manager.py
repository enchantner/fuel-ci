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
Manager for loading drivers as Python modules
"""

from fuel_ci.drivers import localfs
from fuel_ci.drivers import pygit
from fuel_ci.drivers import python_requests
from fuel_ci.drivers import python_sdist
from fuel_ci.drivers import python_tarfile
from fuel_ci.drivers import yaml_parser


class DriverManager(object):

    _index = {
        "parse_datafile": yaml_parser.parse_datafile,

        "download_file_http": python_requests.download_file,
        "pack_tar": python_tarfile.pack,
        #  "pack_cpio": cpio.pack,
        "build_python_package": python_sdist.build,
        #  "build_rpm_package": ,

        "download_artifact": localfs.download_artifact,
        "search_artifact": localfs.search_artifact,
        "publish_artifact": localfs.publish_artifact,

        "git_clone": pygit.repo_clone
    }

    def __init__(self, index=None):
        if index:
            self._index.update(index)

    def __getattr__(self, attr_name):
        if attr_name in self._index:
            return self._index[attr_name]
        else:
            raise NotImplementedError(attr_name)
