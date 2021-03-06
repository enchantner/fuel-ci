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

import logging
import os

from fuel_ci.objects import base

LOG = logging.getLogger(__name__)


class Artifact(base.BaseObject):
    """Artifact object
    """

    #: version
    version = "latest"
    #: version qualifier
    version_qualifier = None
    #: url or localpath
    url = None
    #: metadata
    meta = None
    #: description
    description = None
    #: name of storage object to use
    storage_name = None
    #: comparator to use to determine if new build is needed
    comparator = "artifact_changed"
    #: path
    path = None
    #: whether object is packed
    packed = False

    def __init__(self, **kwargs):
        """Constructs new artifact object

        :param name: name of an artifact specified in YAML
        :param data: artifact data specified in YAML
        :param drivers: dict of driver categories and names to use
        """
        super(Artifact, self).__init__(**kwargs)
        self.content = []

    def add_path(self, path):
        self.content.append(path)

    def add(self, obj):
        self.add_path(obj.path)

    def unpack(self):
        """Call driver specified as "pack" to unpack current artifact
        """
        LOG.debug("Unpacking artifact '{0}'...".format(self))
        self.driver_manager.unpack_tar(self)

    def pack(self):
        """Call driver specified as "pack" to pack current artifact
        """
        LOG.debug("Packing artifact '{0}'...".format(self))
        self.driver_manager.pack_tar(self)
