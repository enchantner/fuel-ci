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

import yaml

from fuel_ci import index

LOG = logging.getLogger(__name__)


def build_index(data):
    """Converts data YAML from dict of strings to dict of
    particular objects.

    :param data: dict of objects parsed from data YAML
    :returns: dict of objects of the same tree as an argument
    """
    data = data.copy()
    ix = index.Index()
    for section in data:
        if section == "scenario":
            ix.set_scenario(load_scenario(data["scenario"]))
            continue
        ix.add_section(section)
        for item in data[section]:
            ix.create_object(section, item)
    return ix


def parse_datafile(filename):
    with open(filename, "r") as conf:
        data = yaml.load(conf.read())
    return build_index(data)


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
