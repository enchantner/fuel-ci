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

"""
Driver for artifact storage based on filesystem
"""

import logging
import os
import shutil

LOG = logging.getLogger(__name__)


class LocalFSDriver(object):
    """Class for local FS artifact storage driver
    """

    def __init__(self, obj):
        """Constructs new local FS driver object

        :param obj: (ArtifactStorage) object with "url" attribute
        """
        self.obj = obj
        self.localpath = obj.url
        if not os.path.exists(self.localpath):
            os.mkdir(self.localpath)

    def _split_version(self, artifact_version):
        art_version = "latest"
        eq = "=="
        if artifact_version[0].isdigit():
            art_version = artifact_version
            eq = "=="
        elif artifact_version.startswith("=="):
            art_version = artifact_version[2:]
            eq = "=="
        else:
            # TODO
            pass
        return eq, art_version

    def list_versions(self, storage, artifact):
        """List versions of a given artifact available in current storage

        :param storage: (ArtifactStorage) object
        :param artifact: (Artifact) object with "name" attribute
        :returns: list of versions (strings)
        """
        versions_path = os.path.join(self.localpath, artifact.name)
        return list(map(lambda v: v.split("-")[1], os.listdir(versions_path)))

    def download_artifact(self, storage, artifact):
        """Search and download given artifact from current storage.
        Copies an artifact from local FS storage to path specified as "path"
        object attribute

        :param storage: (ArtifactStorage) object
        :param artifact: (Artifact) object with "name" and "url" attributes
        :returns: object, passed as artifact
        """
        artifact = self.search_artifact(artifact)
        shutil.copyfile(artifact.url, artifact.path)
        return artifact

    def download_artifact_meta(self, storage, artifact):
        """Search and download given artifact from current storage.
        Sets

        :param storage: (ArtifactStorage) object
        :param artifact: (Artifact) object with "meta", "name" and "url"
               attributes
        :returns: object, passed as artifact
        """
        artifact = self.search_artifact(storage, artifact)
        return artifact

    def search_artifact(self, storage, artifact):
        """Search for given artifact in current storage

        :param storage: (ArtifactStorage) object
        :param artifact: (Artifact) object with "name" and "url" attributes
        :returns: object, passed as artifact, if found
        """
        if artifact.name not in os.listdir(self.localpath):
            raise Exception(
                "Can't find artifact '{0}' in storage '{1}'".format(
                    artifact,
                    self.obj
                )
            )
        versions_path = os.path.join(self.localpath, artifact.name)
        found_path = None

        eq, art_version = self._split_version(artifact.version)

        if eq == "==":
            existing_versions = self.list_versions(storage, artifact)
            if art_version not in existing_versions:
                raise Exception(
                    "Storage '{0}' doesn't include artifact "
                    "'{1}' of specified version".format(
                        self.obj,
                        artifact
                    )
                )
            found_path = os.path.join(
                versions_path,
                "-".join([artifact.name, art_version])
            )
        else:
            # TODO
            pass
        artifact.url = os.path.join(found_path, artifact.name)
        meta_file = os.path.join(found_path, "metadata")
        with open(meta_file, "r") as mf:
            artifact.meta = mf.read()
        return artifact

    def publish_artifact(self, storage, artifact):
        """Publish given artifact in current storage. Copies given artifact
        to local filesystem as binary file + meta.yaml, according to version

        :param storage: (ArtifactStorage) object
        :param artifact: (Artifact) object with "name",
                         "version", "archive", "packed" and "meta" attributes
        :returns: object, passed as artifact, if found
        """
        if not artifact.packed:
            raise Exception("Artifact should be packed before publishing")
        versions_path = os.path.join(self.localpath, artifact.name)
        if not os.path.exists(versions_path):
            os.mkdir(versions_path)

        eq, art_version = self._split_version(artifact.version)
        exact_version_path = os.path.join(
            versions_path,
            "-".join((artifact.name, art_version))
        )
        if not os.path.exists(exact_version_path):
            os.mkdir(exact_version_path)
        # TODO: eq != "=="
        # TODO: "latest"
        art_filename = os.path.join(exact_version_path, artifact.name)
        meta_file = os.path.join(exact_version_path, "metadata")
        shutil.copyfile(artifact.archive, art_filename)
        with open(meta_file, "w") as mf:
            mf.write(artifact.meta)
        return artifact


#: transforming LocalFSDriver class into driver
driver_class = LocalFSDriver
