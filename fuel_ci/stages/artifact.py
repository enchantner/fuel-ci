# -*- coding: utf-8 -*-

"""
Scenarios dealing with artifacts
"""


def download_meta(state):
    """Clones all repos, downloads all artifacts and unpacks them

    :param state: dict of objects loaded from YAML
    """
    for artifact in state["objects"]["artifacts"]:
        artifact_found = False
        for storage in state["objects"]["artifact_storages"]:
            try:
                storage.download_artifact_meta(artifact)
                artifact_found = True
            # TODO: exact exception
            except:
                pass
        if not artifact_found:
            raise Exception(
                "Can't find Artifact {0} "
                "in any of specified storages".format(artifact)
            )
    return state


def download(state):
    """Clones all repos, downloads all artifacts and unpacks them

    :param state: dict of objects loaded from YAML
    """
    for artifact in state["objects"]["artifacts"]:
        artifact_found = False
        for storage in state["objects"]["artifact_storages"]:
            try:
                storage.download_artifact(artifact)
                artifact_found = True
            # TODO: exact exception
            except:
                pass
        if not artifact_found:
            raise Exception(
                "Can't find Artifact {0} "
                "in any of specified storages".format(artifact)
            )
    return state


def unpack(state):
    """TODO

    :param state: dict of objects loaded from YAML
    """

    list(map(lambda a: a.unpack(), state["objects"]["artifacts"]))
    return state


def pack(state):
    """TODO

    :param state: dict of objects loaded from YAML
    """

    list(map(lambda a: a.pack(), state["objects"]["artifacts"]))
    return state


def publish(data):
    """TODO

    :param data: dict of objects loaded from YAML
    """

    list(map(lambda a: a.publish(), data["objects"]["artifacts"]))
    return data
