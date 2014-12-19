# -*- coding: utf-8 -*-


def prepare(objects):
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
    return objects


def test(objects):
    return objects


def publish(objects):
    return objects


def clean(objects):
    return objects
