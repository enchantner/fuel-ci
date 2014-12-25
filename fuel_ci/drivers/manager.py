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

"""
Manager for loading drivers as Python modules
"""


def load_driver(category, driver_name):
    """Imports driver with a given name from a given category.

    :param category: category to import driver from (string)
    :param driver_name: driver name to import (string)
    """
    if driver_name is None:
        return None
    return __import__(
        "fuel_ci.drivers.{0}.{1}".format(
            category,
            driver_name
        ),
        fromlist=[""]
    )


def load_drivers(obj):
    """Imports drivers from a dict in format name:category.

    :param obj: object with "drivers" attribute (dict)
    """
    drv_cache = obj.drivers.copy()
    for cat, driver_name in drv_cache.items():
        driver = load_driver(cat, driver_name)
        if hasattr(driver, "driver_class"):
            driver_object = driver.driver_class(obj)
        else:
            driver_object = driver
        drv_cache[cat] = driver_object
    return drv_cache
