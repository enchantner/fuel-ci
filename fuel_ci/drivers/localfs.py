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
    return os.listdir(versions_path)


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

    if artifact.version_qualifier:
        art_version = "-".join([
            artifact.version,
            artifact.version_qualifier
        ])
    else:
        art_version = artifact.version
    full_name = "-".join([artifact.name, art_version])

    existing_versions = list_versions(localpath, artifact)
    if full_name not in existing_versions:
        raise Exception(
            "Can't find artifact '{0}' ".format(artifact)
        )
    found_path = os.path.join(versions_path, full_name)
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

    art_version_wo_timestamp = artifact.version.split("-")[0]
    art_version = art_version_wo_timestamp + "-{0}".format(time.time())
    full_path = os.path.abspath(
        os.path.join(
            versions_path,
            "-".join([
                artifact.name,
                art_version
            ])
        )
    )

    if os.path.exists(full_path):
        shutil.rmtree(full_path)
    os.mkdir(full_path)

    if artifact.version_qualifier:
        # rewriting symlink for qualifier
        qualifier_path = os.path.abspath(
            os.path.join(
                versions_path,
                "-".join((
                    artifact.name,
                    art_version_wo_timestamp,
                    artifact.version_qualifier
                ))
            )
        )
        if os.path.exists(qualifier_path):
            os.remove(qualifier_path)
        os.symlink(full_path, qualifier_path)

    art_filename = os.path.join(
        full_path,
        artifact.name
    )
    meta_file = os.path.join(full_path, "metadata")
    shutil.copyfile(artifact.archive, art_filename)
    with open(meta_file, "w") as mf:
        if isinstance(artifact.meta, (dict, list)):
            mf.write(yaml.dump(artifact.meta))
        elif isinstance(artifact.meta, six.string_types):
            mf.write(artifact.meta)
    return artifact
