# -*- coding: utf-8 -*-

import logging

from fuel_ci.objects import base

LOG = logging.getLogger(__name__)


class Artifact(base.BaseObject):
    """Artifact object
    """

    #: default dict of driver categories and names to use
    drivers = {
        "compress": None
    }
    #: version
    version = "latest"
    #: url or localpath
    url = None
    #: local path to packed artifact
    archive = None
    #: metadata
    meta = None
    #: description
    description = None

    def __init__(self, name, data, drivers=None):
        """Constructs new artifact object

        :param name: name of an artifact specified in YAML
        :param data: artifact data specified in YAML
        :param drivers: dict of driver categories and names to use
        """
        super(Artifact, self).__init__(data, drivers)
        self.name = name
        self.packed = True

    def unpack(self):
        """Call driver specified as "compress" to unpack current artifact
        """
        LOG.debug("Unpacking artifact '{0}'...".format(self))
        self.drivers["compress"].unpack(self)
        self.packed = False

    def pack(self):
        """Call driver specified as "compress" to pack current artifact
        """
        LOG.debug("Packing artifact '{0}'...".format(self))
        self.drivers["compress"].pack(self)
        self.packed = True
