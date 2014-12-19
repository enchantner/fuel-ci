# -*- coding: utf-8 -*-

import logging

from fuel_ci.objects import base

LOG = logging.getLogger(__name__)


class ArtifactStorage(base.BaseObject):

    drivers = {
        "storage": "localfs"
    }

    def __init__(self, name, data):
        super(ArtifactStorage, self).__init__(data)
        self.name = name

    def download_artifact(self, artifact):
        LOG.debug("Downloading artifact '{0}'...".format(artifact))
        self.drivers["storage"].download_artifact(self, artifact)

    def search_artifact(self, artifact):
        LOG.debug("Searching for artifact '{0}'...".format(artifact))
        self.drivers["storage"].search_artifact(self, artifact)

    def publish_artifact(self, artifact):
        LOG.debug("Publishing artifact '{0}'...".format(artifact))
        self.drivers["storage"].publish_artifact(self, artifact)
