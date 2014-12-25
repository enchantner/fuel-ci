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


class Repository(base.BaseObject):
    """Repository object
    """

    #: default dict of driver categories and names to use
    drivers = {
        "vcs": "git"
    }
    #: default branch to checkout on repo clone
    branch = "master"

    def __init__(self, name, data, drivers=None):
        """Constructs new repository object

        :param name: name of an artifact specified in YAML
        :param data: artifact data specified in YAML
        :param drivers: dict of driver categories and names to use
        """
        super(Repository, self).__init__(data, drivers)
        self.name = name

    def clone(self):
        """Call driver specified as "cvs" to clone current repo
        """
        LOG.debug("Cloning repo '{0}'...".format(self.url))
        self.drivers["vcs"].repo_clone(self)
