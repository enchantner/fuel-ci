# -*- coding: utf-8 -*-

import logging

from fuel_ci.objects import base

LOG = logging.getLogger(__name__)


class Repository(base.BaseObject):
    """Repository object
    """

    #: default dict of driver categories and names to use
    drivers = {
        "cvs": "git"
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
        self.drivers["cvs"].repo_clone(self)
