# -*- coding: utf-8 -*-

import logging

from fuel_ci.objects import base

LOG = logging.getLogger(__name__)


class ArtifactStorage(base.BaseObject):
    """Artifact storage object
    """

    #: default dict of driver categories and names to use
    drivers = {
        "storage": "localfs"
    }

    def __init__(self, name, data, drivers=None):
        """Constructs new artifact storage object

        :param name: name of an artifact specified in YAML
        :param data: artifact data specified in YAML
        :param drivers: dict of driver categories and names to use
        """
        super(ArtifactStorage, self).__init__(data, drivers)
        self.name = name

    def download_artifact(self, artifact):
        """Call driver specified as "storage" to find and download
        specified artifact
        """
        LOG.debug("Downloading artifact '{0}'...".format(artifact))
        self.drivers["storage"].download_artifact(self, artifact)

    def search_artifact(self, artifact):
        """Call driver specified as "storage" to search for
        specified artifact
        """
        LOG.debug("Searching for artifact '{0}'...".format(artifact))
        self.drivers["storage"].search_artifact(self, artifact)

    def publish_artifact(self, artifact):
        """Call driver specified as "storage" to publish specified
        artifact to current storage
        """
        LOG.debug("Publishing artifact '{0}'...".format(artifact))
        self.drivers["storage"].publish_artifact(self, artifact)
