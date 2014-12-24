# -*- coding: utf-8 -*-

"""
Scenario for building package from repo and publishing is
as an artifact
"""


def build(state):
    """Default stage to execute.

    :param state: dict of objects loaded from YAML

    Includes steps:

    - Clone first repository specified in state
      (:meth:`fuel_ci.objects.repo.Repository.clone`)
    - Build a package from repository
      (:meth:`fuel_ci.objects.package.Package.build`)
    - Transform package into a packed artifact
      (:class:`fuel_ci.objects.artifact.Artifact`)
    - Publish artifact in storage specified in objects
      (:meth:`fuel_ci.objects.artifact_storage.ArtifactStorage.\
publish_artifact`)
    """
    package = state["build_objects"]["packages"][0]
    package.build(state["objects"]["repositories"][0])

    build_artifact = state["build_objects"]["artifacts"][0]
    storage = state["objects"]["artifact_storages"][0]
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
    return state
