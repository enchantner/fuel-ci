# -*- coding: utf-8 -*-

import logging

from fuel_ci.objects import base

LOG = logging.getLogger(__name__)


class Package(base.BaseObject):

    drivers = {
        "package": None
    }

    def __init__(self, name, data):
        super(Package, self).__init__(data)
        self.name = name

    def build(self, obj):
        LOG.debug("Creating package '{0}'...".format(self))
        self.drivers["package"].build(self, obj)
