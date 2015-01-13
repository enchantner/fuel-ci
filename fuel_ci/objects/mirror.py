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


class Mirror(base.BaseObject):
    """Mirror object
    """

    #: list of packages
    packages = None

    def __init__(self, **kwargs):
        """Constructs new mirror object

        :param name: name of an mirror specified in YAML
        :param data: mirror data specified in YAML
        :param drivers: dict of driver categories and names to use
        """
        self.built = False
        super(Mirror, self).__init__(**kwargs)

    def set_packages(self, packages):
        self.packages = packages


class RPMMirror(Mirror):

    def build(self):
        """Call driver specified as "repo" to build current mirror
        """
        LOG.debug("Building mirror '{0}'...".format(self))
        self.driver_manager.build_rpm_mirror(self)
        self.built = True


class DEBMirror(Mirror):

    def build(self):
        """Call driver specified as "repo" to build current mirror
        """
        LOG.debug("Building mirror '{0}'...".format(self))
        self.driver_manager.build_deb_mirror(self)
        self.built = True
