# -*- coding: utf-8 -*-

import argparse
import logging
import os

import yaml

from fuel_ci.flow import base

logging.basicConfig(level=logging.DEBUG)

BUILD_DIR = os.getenv("CI_BUILD_DIR") or "build"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "data_file",
        help="YAML data file with entities"
    )
    params, other_params = parser.parse_known_args()

    data_file = params.data_file
    if not os.path.exists(data_file):
        raise Exception(
            "data file '{0}' does not exist".format(data_file)
        )

    with open(data_file, "r") as conf:
        data = yaml.load(conf.read())

    if not "flow" in data:
        Flow = base.BaseFlow
    else:
        flow_module, flow_class = data["flow"].split(":")
        Flow = getattr(__import__(
            flow_module,
            fromlist=[""]
        ), flow_class, None)

    Flow(data, BUILD_DIR).run()


if __name__ == "__main__":
    main()
