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

from fuel_ci.objects import base

LOG = logging.getLogger(__name__)


class Package(base.BaseObject):
    """Package object
    """

    #: default dict of driver categories and names to use
    drivers = {
        "package": None
    }

    def build(self, obj):
        """Call driver specified as "package" to build package
        in desired format
        """
        LOG.debug("Creating package '{0}'...".format(self))
        self.drivers["package"].build(self, obj)
