# -*- coding: utf-8 -*-

import pygit2


def repo_clone(repo):
    # TODO: if exists
    return pygit2.clone_repository(
        repo.url,
        repo.path,
        checkout_branch=repo.branch
    )


def repo_status(repo):
    try:
        pygit2.discover_repository(repo.path)
    except KeyError:
        return False
    return True
