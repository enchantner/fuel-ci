# -*- coding: utf-8 -*-

from itertools import starmap
import logging

import yaml

from fuel_ci.objects import artifact
from fuel_ci.objects import artifact_storage
from fuel_ci.objects import repo
from fuel_ci.objects import package
from fuel_ci.objects import mirror

LOG = logging.getLogger(__name__)


def parse_objects(data):
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
        "packages": package.Package,
        "mirror": mirror.Mirror
    }.items():
        for section in ("objects", "build_objects"):
            if entity in res[section]:
                res[section][entity] = _build_objects(section, entity, c)
    return res


def parse_datafile(filename):
    with open(filename, "r") as conf:
        data = yaml.load(conf.read())
    return parse_objects(data)


def load_scenario(data):
    """Load scenarios specified in data (in YAML)

    :param data: dict of objects parsed from data YAML
    """
    scenario = data["scenario"]
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
