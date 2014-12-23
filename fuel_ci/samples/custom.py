# -*- coding: utf-8 -*-

import os

from fuel_ci.stages.artifact import download_meta
from fuel_ci.stages.artifact import pack


def compare_meta(state):
    state = download_meta(state)
    return state


def pack_artifact(state):
    repo = state["objects"]["repositories"][0]
    artifact = state["build_objects"]["artifacts"][0]
    storage = state["objects"]["artifact_storages"][0]

    packages_file = os.path.join(repo.path, "sample_packages.txt")
    with open(packages_file, "r") as p:
        artifact.meta = {"packages": p.read().split()}
    artifact.path = packages_file
    artifact.pack()
    storage.publish(artifact)
    return state
