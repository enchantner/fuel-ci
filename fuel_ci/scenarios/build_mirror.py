# -*- coding: utf-8 -*-

import os
import yaml


def scenario(data):
    repo = data["objects"]["repositories"][0]
    storage = data["objects"]["artifact_storages"][0]
    mirror = data["build_objects"]["mirror"][0]
    artifact = data["build_objects"]["artifacts"][0]

    repo.clone()
    if "packages_file" in repo.meta:
        packages_file = os.path.join(repo.path, repo.meta["packages_file"])
        with open(packages_file, "r") as p:
            mirror.set_packages(p.read().split())

    artifact.add(mirror)
    artifact.meta = yaml.dump({"packages": mirror.packages})
    artifact.pack()
    storage.publish_artifact(artifact)
