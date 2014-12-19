# -*- coding: utf-8 -*-

import logging

from fuel_ci.objects import base

LOG = logging.getLogger(__name__)


class Artifact(base.BaseObject):

    drivers = {
        "compress": None
    }
    version = "latest"
    url = None
    meta = None

    def __init__(self, name, data, drivers=None):
        super(Artifact, self).__init__(data, drivers)
        self.name = name
        self.packed = True

    def unpack(self):
        LOG.debug("Unpacking artifact '{0}'...".format(self))
        self.drivers["compress"].unpack(self)
        self.packed = False

    def pack(self):
        LOG.debug("Packing artifact '{0}'...".format(self))
        self.drivers["compress"].pack(self)
        self.packed = True
