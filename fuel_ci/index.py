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

from fuel_ci.objects import artifact
from fuel_ci.objects import artifact_storage
from fuel_ci.objects import repo
from fuel_ci.objects import package
from fuel_ci.objects import mirror


class ObjectIndex(object):

    REPOSITORIES_TYPES = (
        "git",
    )

    def __init__(self, data):
        # TODO: rewrite to using metaclasses
        self.obj_classes = {
            "artifact": artifact.Artifact,
            "artifact_storage": artifact_storage.ArtifactStorage,
            "git": repo.GitRepository,
            "package": package.Package,
            "mirror": mirror.Mirror
        }
        self.main_scenario = None

        for section in data:
            if section == "scenario":
                self.set_scenario(self.load_scenario(data["scenario"]))
                continue
            self.add_section(section)
            for item in data[section]:
                self.create_object(section, item)

    def load_scenario(scenario):
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

    def filter(self, section, **kwargs):
        return list(filter(
            lambda o: all(
                list(map(lambda k, v: getattr(o, k) == v,
                         kwargs.items()))
            ),
            getattr(self, section)
        ))

    def create_object(self, section, item):
        self.add_object(
            section,
            self.obj_classes[item["type"]](**item)
        )

    def add_object(self, section, obj):
        getattr(self, section).append(obj)

    def add_section(self, section):
        setattr(self, section, [])

    def set_scenario(self, scenario):
        self.main_scenario = scenario

    def repositories(self, section="objects"):
        return list(filter(
            lambda o: o.type in self.REPOSITORIES_TYPES,
            getattr(self, section)
        ))

    def artifact_storages(self, section="objects"):
        return list(filter(
            lambda o: o.type == "artifact_storage",
            getattr(self, section)
        ))

    def artifacts(self, section="objects"):
        return list(filter(
            lambda o: o.type == "artifact",
            getattr(self, section)
        ))

    def mirrors(self, section="objects"):
        return list(filter(
            lambda o: o.type == "mirror",
            getattr(self, section)
        ))

    def packages(self, section="objects"):
        return list(filter(
            lambda o: o.type == "package",
            getattr(self, section)
        ))
