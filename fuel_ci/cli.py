# -*- coding: utf-8 -*-

import argparse
import logging
import os

from fuel_ci.drivers import manager as driver_manager

logging.basicConfig(level=logging.DEBUG)

BUILD_DIR = os.getenv("CI_BUILD_DIR") or "build"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--data', dest='data', action='store', type=str,
        help='data parser to use', default='yaml_parser'
    )
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

    data_driver = driver_manager.load_driver(
        "data",
        params.data
    )
    data = data_driver.parse_datafile(data_file)
    scenario = data_driver.load_scenario(data)
    scenario(data)


if __name__ == "__main__":
    main()
