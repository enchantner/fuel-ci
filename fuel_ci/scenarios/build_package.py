# -*- coding: utf-8 -*-

"""
Scenario for building package from repo and publishing is
as an artifact
"""


def build(objects):
    """Default stage to execute.

    :param objects: dict of objects loaded from YAML

    Includes steps:

    - Clone first repository specified in objects
      (:meth:`fuel_ci.objects.repo.Repository.clone`)
    - Build a package from repository
      (:meth:`fuel_ci.objects.package.Package.build`)
    - Transform package into a packed artifact
      (:class:`fuel_ci.objects.artifact.Artifact`)
    - Publish artifact in storage specified in objects
      (:meth:`fuel_ci.objects.artifact_storage.ArtifactStorage.\
publish_artifact`)
    """
    repo = objects["repositories"][0]
    repo.clone()
    package = objects["packages"][0]
    package.build(repo)

    build_artifact = objects["build_artifacts"][0]
    storage = objects["artifact_storages"][0]
    if storage.name != build_artifact.storage:
        raise Exception(
            "Storage name '{0}' differs from the one "
            "specified in build_artifact: '{1}'".format(
                storage.name,
                build_artifact.name
            )
        )
    build_artifact.archive = package.path
    if not build_artifact.packed:
        build_artifact.pack()
    build_artifact.meta = {
        "version": build_artifact.version,
        "description": build_artifact.description
    }
    storage.publish_artifact(build_artifact)
    return objects
