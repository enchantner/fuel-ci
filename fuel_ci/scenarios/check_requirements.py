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

from fuel_ci.objects.artifact import Artifact

from fuel_ci.scenarios.actions.storage import find_storage_for_artifact
from fuel_ci.scenarios.compare.artifact import changed as artifact_changed


def scenario(obj_manager):
    build_required = False

    artifact_to_build = obj_manager.lookup(
        obj_manager.lookup_by_class(Artifact),
        build=True
    )[0]
    build_storage = find_storage_for_artifact(
        obj_manager,
        artifact_to_build
    )

    try:
        build_storage.download_artifact_meta(artifact_to_build)
    # TODO: exact custom exception - artifact not found
    except Exception:
        build_required = True

    if not build_required:
        artifacts_check_changed = obj_manager.lookup(
            comparator="artifact_changed",
            dependency=True
        )
        for art in artifacts_check_changed:
            art_storage = find_storage_for_artifact(obj_manager, art)
            art_storage.download_artifact_meta(art)
            if artifact_changed(art, artifact_to_build):
                build_required = True
                break

    if not build_required:
        raise Exception("No changes - nothing to rebuild")
