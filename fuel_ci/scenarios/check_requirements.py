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

from fuel_ci.scenarios.actions import storage
from fuel_ci.scenarios.compare import artifact


COMPARATORS = {
    "artifact_changed": artifact.changed
}


def scenario(obj_manager):
    artifacts_check_changed = obj_manager.lookup(
        comparator="artifact_changed",
        dependency=True
    )
    for art in artifacts_check_changed:
        art_storage = storage.find_storage_for_artifact(obj_manager, art)
        try:
            art_storage.search_artifact(art)
        except Exception as exc:
            pass
        art_storage.download_artifact_meta(art)
        print(art.meta)

    # for f, comparator in comparators.items():
    #     artifacts
    #     list(map(
    #         comparator,
    #         obj_manager.lookup(artifact_changed=True)
    #     ))
