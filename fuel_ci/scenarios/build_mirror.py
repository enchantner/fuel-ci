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
import yaml


def scenario(data):
    repo = data["objects"]["repositories"][0]
    storage = data["objects"]["artifact_storages"][0]
    mirror = data["build_objects"]["mirror"][0]
    artifact = data["build_objects"]["artifacts"][0]

    repo.clone()
    if "packages_file" in repo.meta:
        packages_file = os.path.join(repo.path, repo.meta["packages_file"])
        with open(packages_file, "r") as p:
            mirror.set_packages(p.read().split())

    artifact.add(mirror)
    artifact.meta = yaml.dump({"packages": mirror.packages})
    artifact.pack()
    storage.publish_artifact(artifact)
