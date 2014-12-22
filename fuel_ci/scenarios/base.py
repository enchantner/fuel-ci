# -*- coding: utf-8 -*-

"""
Base scenario for artifact-based build. Includes 5 stages:

1. prepare
2. build
3. test
4. publish
5. clean
"""


def prepare(objects):
    """Clones all repos, downloads all artifacts and unpacks them

    :param objects: dict of objects loaded from YAML
    """

    # list(map(lambda r: r.clone(), repos))
    storage = None
    for art in objects["artifacts"]:
        if art.storage:
            find_storage = filter(
                lambda strg: strg.name == art.storage,
                objects["artifact_storages"]
            )
            if find_storage:
                storage = find_storage[0]
                storage.download_artifact(art)
        else:
            # TODO: search all storages if no storage specified
            pass

    art = objects["artifacts"][0]
    art.version = "0.2"
    art.pack()
    storage.publish_artifact(art)

    # list(map(lambda a: a.download(), objects["artifacts"]))
    # list(map(lambda a: a.unpack(), artifacts))
    return objects


def build(objects):
    """TODO

    :param objects: dict of objects loaded from YAML
    """
    return objects


def test(objects):
    """TODO

    :param objects: dict of objects loaded from YAML
    """
    return objects


def publish(objects):
    """TODO

    :param objects: dict of objects loaded from YAML
    """
    return objects


def clean(objects):
    """TODO

    :param objects: dict of objects loaded from YAML
    """
    return objects
