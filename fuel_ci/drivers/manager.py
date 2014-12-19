# -*- coding: utf-8 -*-


def load_driver(category, driver_name):
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
    drv_cache = obj.drivers.copy()
    for cat, driver_name in drv_cache.items():
        driver = load_driver(cat, driver_name)
        if hasattr(driver, "driver_class"):
            driver_object = driver.driver_class(obj)
        else:
            driver_object = driver
        drv_cache[cat] = driver_object
    return drv_cache
