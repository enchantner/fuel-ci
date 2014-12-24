# -*- coding: utf-8 -*-

"""
Driver for creating tar archives
"""

import tarfile


def pack(obj):
    """Pack object into tar archive

    :param obj: (Artifact) object with "name" and "archive" attributes
    """
    tar = tarfile.open(obj.name, "w")
    for path in obj.content:
        # TODO: check if file or directory
        tar.add(path)
    tar.close()
    obj.archive = obj.name


def unpack(obj):
    """Unpack tar archive

    :param obj: object with "archive" attribute
    """
    pass
