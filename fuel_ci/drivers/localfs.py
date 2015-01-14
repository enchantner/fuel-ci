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
import time

import six

import yaml

LOG = logging.getLogger(__name__)


def _split_version(artifact_version):
    art_version = "latest"
    eq = "=="
    if artifact_version[0].isdigit():
        art_version = artifact_version
        eq = "=="
    elif artifact_version.startswith("=="):
        eq = "=="
    else:
        # TODO
        pass
    return eq, art_version


def _ensure_dir_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def list_versions(localpath, artifact):
    """List versions of a given artifact available in current storage

    :param storage: (ArtifactStorage) object
    :param artifact: (Artifact) object with "name" attribute
    :returns: list of versions (strings)
    """
    _ensure_dir_exists(localpath)
    versions_path = os.path.join(localpath, artifact.name)
    return list(map(lambda v: v.split("-")[1], os.listdir(versions_path)))


def download_artifact(localpath, artifact):
    """Search and download given artifact from current storage.
    Copies an artifact from local FS storage to path specified as "path"
    object attribute

    :param storage: (ArtifactStorage) object
    :param artifact: (Artifact) object with "name" and "url" attributes
    :returns: object, passed as artifact
    """
    _ensure_dir_exists(localpath)
    artifact = search_artifact(localpath, artifact)
    shutil.copyfile(artifact.url, artifact.path)
    return artifact


def download_artifact_meta(localpath, artifact):
    """Search and download given artifact from current storage.
    Sets

    :param storage: (ArtifactStorage) object
    :param artifact: (Artifact) object with "meta", "name" and "url"
           attributes
    :returns: object, passed as artifact
    """
    _ensure_dir_exists(localpath)
    artifact = search_artifact(localpath, artifact)
    return artifact


def search_artifact(localpath, artifact):
    """Search for given artifact in current storage

    :param storage: (ArtifactStorage) object
    :param artifact: (Artifact) object with "name" and "url" attributes
    :returns: object, passed as artifact, if found
    """
    _ensure_dir_exists(localpath)
    if artifact.name not in os.listdir(localpath):
        raise Exception(
            "Can't find artifact '{0}'".format(artifact)
        )
    versions_path = os.path.join(localpath, artifact.name)
    found_path = None

    eq, art_version = _split_version(artifact.version)

    if eq == "==":
        existing_versions = list_versions(localpath, artifact)
        if art_version not in existing_versions:
            raise Exception(
                "Can't find artifact '{0}' ".format(artifact)
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
        meta_content = mf.read()
        try:
            artifact.meta = yaml.load(meta_content)
        except yaml.ParserError:
            artifact.meta = meta_content
    return artifact


def publish_artifact(localpath, artifact):
    """Publish given artifact in current storage. Copies given artifact
    to local filesystem as binary file + meta.yaml, according to version

    :param artifact: (Artifact) object with "name",
                     "version", "archive", "packed" and "meta" attributes
    :returns: object, passed as artifact, if found
    """
    _ensure_dir_exists(localpath)
    if not artifact.packed:
        raise Exception("Artifact should be packed before publishing")

    versions_path = os.path.join(localpath, artifact.name)

    _ensure_dir_exists(versions_path)

    eq, art_version = _split_version(artifact.version)
    art_version_wo_timestamp = art_version.split("-")[0]
    art_version = art_version_wo_timestamp + "-{0}".format(time.time())

    # rewriting symlink for current version
    latest_version_path = os.path.abspath(
        os.path.join(
            versions_path,
            "-".join((
                artifact.name,
                art_version_wo_timestamp,
                "latest"
            ))
        )
    )
    if os.path.exists(latest_version_path):
        os.remove(latest_version_path)

    exact_version_path = os.path.abspath(
        os.path.join(
            versions_path,
            "-".join((artifact.name, art_version))
        )
    )
    _ensure_dir_exists(exact_version_path)

    os.symlink(exact_version_path, latest_version_path)

    # TODO: eq != "=="
    art_filename = os.path.join(
        exact_version_path,
        artifact.name
    )
    meta_file = os.path.join(exact_version_path, "metadata")
    shutil.copyfile(artifact.archive, art_filename)
    with open(meta_file, "w") as mf:
        if isinstance(artifact.meta, (dict, list)):
            mf.write(yaml.dump(artifact.meta))
        elif isinstance(artifact.meta, six.string_type):
            mf.write(artifact.meta)
    return artifact
