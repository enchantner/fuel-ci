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

from fuel_ci.scenarios import check_requirements

from fuel_ci.scenarios.actions.storage import find_storage_for_artifact


def scenario(obj_manager):
    check_requirements.scenario(obj_manager)

    build_artifact = obj_manager.lookup(build=True)[0]
    artifact_deps = obj_manager.lookup(dependency=True)
    for art in artifact_deps:
        art_storage = find_storage_for_artifact(obj_manager, art)
        art_storage.download_artifact(art)
        art.unpack()
        build_artifact.add_path(art.unpacked_path)

    build_artifact.pack()
    build_storage = find_storage_for_artifact(obj_manager, build_artifact)
    build_storage.publish_artifact(build_artifact)
    return obj_manager
