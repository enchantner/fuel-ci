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
        "config_file",
        help="YAML config file"
    )
    params, other_params = parser.parse_known_args()

    config_file = params.config_file
    if not os.path.exists(config_file):
        raise Exception(
            "config file '{0}' does not exist".format(config_file)
        )

    with open(config_file, "r") as conf:
        config = yaml.load(conf.read())

    if not "flow" in config:
        Flow = base.BaseFlow
    else:
        flow_module, flow_class = config["flow"].split(":")
        Flow = getattr(__import__(
            flow_module,
            fromlist=[""]
        ), flow_class, None)

    Flow(config, BUILD_DIR).run()


if __name__ == "__main__":
    main()
