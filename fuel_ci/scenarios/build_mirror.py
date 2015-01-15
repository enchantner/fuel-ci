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

import os

from fuel_ci.objects.repo import Repository
from fuel_ci.objects.artifact_storage import ArtifactStorage
from fuel_ci.objects.mirror import Mirror
from fuel_ci.objects.artifact import Artifact


def scenario(obj_manager):
    clone_repos = obj_manager.lookup_by_class(Repository)

    mirror = obj_manager.lookup_by_class(Mirror)[0]

    list(map(lambda r: r.clone(), clone_repos))

    for repo in clone_repos:
        if "packages_file" in repo.meta:
            packages_file = os.path.join(repo.path, repo.meta["packages_file"])
            with open(packages_file, "r") as p:
                mirror.set_packages(p.read().split())

    artifact = obj_manager.lookup(
        obj_manager.lookup_by_class(Artifact),
        build=True
    )[0]
    artifact.add(mirror)
    artifact.meta = {"packages": mirror.packages}
    artifact.pack()

    storage = obj_manager.lookup(
        obj_manager.lookup_by_class(ArtifactStorage),
        build=False,
    )[0]
    storage.publish_artifact(artifact)
    return obj_manager
