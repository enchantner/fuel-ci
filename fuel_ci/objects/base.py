# -*- coding: utf-8 -*-

from fuel_ci.drivers import manager as driver_manager


class BaseObject(object):

    drivers = {}

    def __init__(self, data, drivers=None):
        self.update(**data)
        if drivers:
            self.drivers = drivers
        self.drivers = driver_manager.load_drivers(self)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
