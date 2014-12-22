# -*- coding: utf-8 -*-

from fuel_ci.drivers import manager as driver_manager


class BaseObject(object):
    """Base object implementation
    """

    #: default dict of driver categories and names to use
    drivers = {}

    def __init__(self, data, drivers=None):
        """Constructor for base object

        :param data: artifact data specified in YAML
        :param drivers: dict of driver categories and names to use
        """
        self.update(**data)
        if drivers:
            self.drivers = drivers
        self.drivers = driver_manager.load_drivers(self)

    def update(self, **kwargs):
        """Update current object fields according to specified arguments
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
