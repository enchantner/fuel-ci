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

import yaml

"""
Scenario for building package from repo and publishing is
as an artifact
"""


def build(state):
    """Default stage to execute.

    :param state: dict of objects loaded from YAML

    Includes steps:

    - Clone first repository specified in state
      (:meth:`fuel_ci.objects.repo.Repository.clone`)
    - Build a package from repository
      (:meth:`fuel_ci.objects.package.Package.build`)
    - Transform package into a packed artifact
      (:class:`fuel_ci.objects.artifact.Artifact`)
    - Publish artifact in storage specified in objects
      (:meth:`fuel_ci.objects.artifact_storage.ArtifactStorage.\
publish_artifact`)
    """
    package = state["build_objects"]["packages"][0]
    package.build(state["objects"]["repositories"][0])
    build_artifact = state["build_objects"]["artifacts"][0]
    storage = state["objects"]["artifact_storages"][0]

    build_artifact.add(package)
    if not build_artifact.packed:
        build_artifact.pack()
    build_artifact.meta = yaml.dump({
        "version": build_artifact.version,
        "description": build_artifact.description
    })
    storage.publish_artifact(build_artifact)
    return state
