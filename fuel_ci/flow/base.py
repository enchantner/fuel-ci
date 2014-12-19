# -*- coding: utf-8 -*-

import abc
from functools import reduce
from itertools import starmap

import six

from fuel_ci.objects import artifact
from fuel_ci.objects import artifact_storage
from fuel_ci.objects import repo
from fuel_ci.objects import package
from fuel_ci.scenarios import base as base_scenario


@six.add_metaclass(abc.ABCMeta)
class AbstractFlow(object):

    @abc.abstractmethod
    def run(self):
        pass


class BaseFlow(AbstractFlow):

    def __init__(self, data, build_dir, scenario=None):
        self.objects = self._load_objects(data)
        self.build_dir = build_dir
        self._stages = []

        if not scenario and "scenario" in data:
            for stage in data["scenario"]:
                method_path = stage.split(".")
                if len(method_path) == 1:
                    method = "build"
                else:
                    method = method_path[1]
                module = __import__(
                    "fuel_ci.scenarios.{0}".format(stage),
                    fromlist=[""]
                )
                self.add_stage(getattr(module, method))
        else:
            self.set_scenario(scenario or (
                base_scenario.prepare,
                base_scenario.build,
                base_scenario.test,
                base_scenario.publish,
                base_scenario.clean
            ))

    def _load_objects(self, data):
        res = data.copy()
        _build_objects = lambda key, c: list(
            starmap(c, res[key].items())
        )
        for entity, c in {
            "artifacts": artifact.Artifact,
            "artifact_storages": artifact_storage.ArtifactStorage,
            "repositories": repo.Repository,
            "packages": package.Package
        }.items():
            if entity in res:
                res[entity] = _build_objects(entity, c)
        return res

    def set_scenario(self, stages):
        self._stages = stages

    def add_stage(self, stage):
        self._stages.append(stage)

    def run(self):
        last_result = self.objects
        for stage in self._stages:
            last_result = stage(last_result)
        return last_result
