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

import logging

from fuel_ci.objects.artifact_storage import ArtifactStorage

LOG = logging.getLogger(__name__)


def find_storage_for_artifact(obj_manager, art):
    check_storages = []
    if art.storage_name:
        check_storages.extend(
            obj_manager.lookup(
                obj_manager.lookup_by_class(ArtifactStorage),
                name=art.storage_name
            )
        )
    else:
        check_storages.extend(
            obj_manager.lookup_by_class(ArtifactStorage)
        )

    if check_storages:
        return check_storages[0]

    raise Exception(
        "Can't find storage for artifact '{0}'".format(art)
    )
