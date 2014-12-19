# -*- coding: utf-8 -*-

import logging

from fuel_ci.objects import base

LOG = logging.getLogger(__name__)


class Repository(base.BaseObject):

    drivers = {
        "cvs": "git"
    }
    branch = "master"

    def __init__(self, name, data):
        super(Repository, self).__init__(data)
        self.name = name

    def clone(self):
        LOG.debug("Cloning repo '{0}'...".format(self.url))
        self.drivers["cvs"].repo_clone(self)
