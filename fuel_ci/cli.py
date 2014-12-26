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
    index = data_driver.parse_datafile(data_file)
    index.main_scenario(index)


if __name__ == "__main__":
    main()
