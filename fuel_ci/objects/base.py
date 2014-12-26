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

from fuel_ci.drivers import manager as driver_manager


class BaseObject(object):
    """Base object implementation
    """

    #: default dict of driver categories and names to use
    drivers = {}

    def __init__(self, **kwargs):
        """Constructor for base object

        :param data: artifact data specified in YAML
        :param drivers: dict of driver categories and names to use
        """
        self.update(**kwargs)
        if "drivers" in kwargs:
            self.drivers = kwargs["drivers"]
        self.drivers = driver_manager.load_drivers(self)

    def update(self, **kwargs):
        """Update current object fields according to specified arguments
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
