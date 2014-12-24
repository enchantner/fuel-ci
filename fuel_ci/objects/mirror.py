# -*- coding: utf-8 -*-

import logging

from fuel_ci.objects import base

LOG = logging.getLogger(__name__)


class Mirror(base.BaseObject):
    """Mirror object
    """

    #: default dict of driver categories and names to use
    drivers = {
        "mirror": None
    }
    #: list of packages
    packages = None

    def __init__(self, name, data, drivers=None):
        """Constructs new mirror object

        :param name: name of an mirror specified in YAML
        :param data: mirror data specified in YAML
        :param drivers: dict of driver categories and names to use
        """
        super(Mirror, self).__init__(data, drivers)
        self.name = name
        self.built = False

    def set_packages(self, packages):
        self.packages = packages

    def build(self):
        """Call driver specified as "repo" to build current mirror
        """
        LOG.debug("Building mirror '{0}'...".format(self))
        self.drivers["mirror"].build(self)
        self.built = True
