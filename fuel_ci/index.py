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


class Index(object):

    REPOSITORIES_TYPES = (
        "git",
    )

    def __init__(self, sections=None):
        if sections:
            list(map(self.add_section, sections))

        # TODO: rewrite to using metaclasses
        self.obj_classes = {
            "artifact": artifact.Artifact,
            "artifact_storage": artifact_storage.ArtifactStorage,
            "git": repo.GitRepository,
            "package": package.Package,
            "mirror": mirror.Mirror
        }
        self.main_scenario = None

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
