# -*- coding: utf-8 -*-

"""
Driver for creating tar archives
"""

import os
import tarfile


def pack(obj):
    """Pack object into tar archive

    :param obj: object with "path" attribute
    """
    tar = tarfile.open(obj.path, "w")
    for name in os.path.listdir(obj.path):
        tar.add(name)
    tar.close()


def unpack(obj):
    """Unpack tar archive

    :param obj: object with "archive" attribute
    """
    pass
