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
Driver for creating tar archives
"""

import os
import shutil
import tarfile


def pack(obj):
    """Pack object into tar archive

    :param obj: (Artifact) object with "name" and "archive" attributes
    """
    tar = tarfile.open(obj.path, "w")
    for path in obj.content:
        # TODO: check if file or directory
        tar.add(path)
    tar.close()
    obj.archive = obj.path
    obj.packed = True


def unpack(obj):
    """Unpack tar archive

    :param obj: object with "archive" attribute
    """
    tar = tarfile.open(obj.path)
    if os.path.exists(obj.unpacked_path):
        shutil.rmtree(obj.unpacked_path)
    os.mkdir(obj.unpacked_path)
    tar.extractall(obj.unpacked_path)
    tar.close()
    obj.packed = False
