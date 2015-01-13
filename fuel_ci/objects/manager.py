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
Manager for loading objects
"""

import logging

from fuel_ci.objects import artifact
from fuel_ci.objects import artifact_storage
from fuel_ci.objects import repo
from fuel_ci.objects import package
from fuel_ci.objects import mirror

LOG = logging.getLogger(__name__)


class ObjectManager(object):

    REPOSITORIES_TYPES = (
        "git",
    )

    _index = []

    def __init__(self, data, driver_manager):
        # TODO: rewrite to using metaclasses
        self.obj_classes = {
            "artifact": artifact.Artifact,
            "artifact_storage": artifact_storage.ArtifactStorage,
            "localfs": artifact_storage.LocalArtifactStorage,
            "git": repo.GitRepository,
            "package": package.Package,
            "mirror": mirror.Mirror
        }
        self.main_scenario = None
        self.driver_manager = driver_manager

        self.set_scenario(self.load_scenario(data["scenario"]))

        for item in data["objects"]:
            self.create_object(item)

    def load_scenario(self, scenario):
        """Load scenarios specified as path to Python module

        :param scenario: path to scenario as "my_package.my_module.my_scenario"
        """
        third_party = False
        method_path = scenario.split(".")
        method_path_len = len(method_path)
        if method_path_len == 1:
            method = "scenario"
        elif method_path_len == 2:
            scenario, method = method_path
        else:
            third_party = True
            method = method_path.pop()
            scenario = ".".join(method_path)
        LOG.debug(
            "Preparing scenario {0}.{1}...".format(
                scenario,
                method
            )
        )
        if not third_party:
            scenario = "fuel_ci.scenarios.{0}".format(scenario)
        module = __import__(
            scenario,
            fromlist=[""]
        )
        return getattr(module, method)

    def create_object(self, item):
        self.add_object(
            self.obj_classes[item["type"]](
                driver_manager=self.driver_manager,
                **item
            )
        )

    def add_object(self, obj):
        self._index.append(obj)

    def set_scenario(self, scenario):
        self.main_scenario = scenario

    def lookup(self, index=None, **kwargs):
        use_index = index or self._index
        return list(filter(
            lambda o: all(
                list(map(
                    lambda kv: getattr(o, kv[0]) == kv[1],
                    kwargs.items())
                )
            ),
            use_index
        ))

    def lookup_by_class(self, cls, index=None):
        use_index = index or self._index
        return list(filter(
            lambda o: isinstance(o, cls),
            use_index
        ))
