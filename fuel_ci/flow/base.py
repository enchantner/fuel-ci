# -*- coding: utf-8 -*-

"""
AbstractFlow and BaseFlow definitions
"""

import abc
from itertools import starmap
import logging

import six

from fuel_ci.objects import artifact
from fuel_ci.objects import artifact_storage
from fuel_ci.objects import repo
from fuel_ci.objects import package

LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class AbstractFlow(object):
    """Abstract flow object
    """

    @abc.abstractmethod
    def run(self):
        """Abstract scenario runner
        """
        pass


class BaseFlow(AbstractFlow):
    """Base flow object. Implements linear scenario -
    all stages are run one after another and result of
    previous stage is passed to the next one.
    """

    def __init__(self, data, build_dir, scenario=None):
        """Constructs new BaseFlow object.

        :param data: dict of objects parsed from data YAML
        :param build_dir: working directory for build
        :param scenario: list of callable stages to execute
        """

        self.state = self._load_objects(data)
        self.build_dir = build_dir
        self._stages = []

        if not scenario and "scenario" in data:
            self._load_scenario(data)
        elif scenario:
            self.set_scenario(scenario)
        else:
            raise Exception("No scenario to execute")

    def _load_scenario(self, data):
        """Load scenarios specified in data (in YAML)

        :param data: dict of objects parsed from data YAML
        """
        for stage in data["scenario"]:
            third_party = False
            method_path = stage.split(".")
            method_path_len = len(method_path)
            if method_path_len == 1:
                method = "build"
            elif method_path_len == 2:
                stage, method = method_path
            else:
                third_party = True
                method = method_path.pop()
                stage = ".".join(method_path)

            # TODO: external
            LOG.debug(
                "Preparing stage {0}.{1}...".format(
                    stage,
                    method
                )
            )
            if not third_party:
                stage = "fuel_ci.stages.{0}".format(stage)
            module = __import__(
                stage,
                fromlist=[""]
            )
            self.add_stage(getattr(module, method))

    def _load_objects(self, data):
        """Converts data YAML from dict of strings to dict of
        particular objects.

        :param data: dict of objects parsed from data YAML
        :returns: dict of objects of the same tree as an argument
        """
        res = data.copy()
        _build_objects = lambda section, key, c: list(
            starmap(c, res[section][key].items())
        )
        for entity, c in {
            "artifacts": artifact.Artifact,
            "build_artifacts": artifact.Artifact,
            "artifact_storages": artifact_storage.ArtifactStorage,
            "repositories": repo.Repository,
            "packages": package.Package
        }.items():
            for section in ("objects", "build_objects"):
                if entity in res[section]:
                    res[section][entity] = _build_objects(section, entity, c)
        return res

    def set_scenario(self, stages):
        """Sets scenario (list of stages) to execute in current flow.

        :param stages: list of callable stages
        """
        self._stages = stages

    def add_stage(self, stage):
        """Appends stage to execute at the end of existing stage list.

        :param stages: list of callable stages
        """
        self._stages.append(stage)

    def run(self):
        """Runner method which implements linear scenario for stages
        defined in current flow - all stages are run one after another
        and result of previous stage is passed to the next one.

        :returns: result of the last stage in list
        """
        last_result = self.state
        for stage in self._stages:
            last_result = stage(last_result)
        return last_result
