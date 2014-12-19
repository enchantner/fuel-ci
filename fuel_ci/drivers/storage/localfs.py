# -*- coding: utf-8 -*-

import logging
import os
import shutil

import yaml

LOG = logging.getLogger(__name__)


class LocalFSDriver(object):

    def __init__(self, obj):
        self.obj = obj
        self.localpath = obj.url

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
        versions_path = os.path.join(self.localpath, artifact.name)
        return list(map(lambda v: v.split("-")[1], os.listdir(versions_path)))

    def download_artifact(self, storage, artifact):
        artifact = self.search_artifact(artifact)
        shutil.copyfile(artifact.url, artifact.path)
        return artifact

    def search_artifact(self, storage, artifact):
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
        meta_file = os.path.join(found_path, "meta.yaml")
        with open(meta_file, "r") as mf:
            artifact.meta = yaml.load(mf.read())
        return artifact

    def publish_artifact(self, artifact):
        if not artifact.packed:
            raise Exception("")
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
        meta_file = os.path.join(exact_version_path, "meta.yaml")
        shutil.copyfile(artifact.archive, art_filename)
        with open(meta_file, "w") as mf:
            mf.write(yaml.dump(artifact.meta))
        return artifact


driver_class = LocalFSDriver
