# -*- coding: utf-8 -*-

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

    def __init__(self, name, data, drivers=None):
        """Constructs new package object

        :param name: name of a package specified in YAML
        :param data: package data specified in YAML
        :param drivers: dict of driver categories and names to use
        """
        super(Package, self).__init__(data, drivers)
        self.name = name

    def build(self, obj):
        """Call driver specified as "package" to build package
        in desired format
        """
        LOG.debug("Creating package '{0}'...".format(self))
        self.drivers["package"].build(self, obj)
