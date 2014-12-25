# -*- coding: utf-8 -*-

import setuptools

import pbr
import pbr.packaging


# this monkey patch is to avoid appending git version to version
pbr.packaging._get_version_from_git = lambda pre_version: pre_version


setuptools.setup(
    setup_requires=['pbr'],
    pbr=True)
