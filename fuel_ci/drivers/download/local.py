# -*- coding: utf-8 -*-

import shutil


def download_artifact(artifact):
    shutil.copytree(artifact.url, artifact.path)
