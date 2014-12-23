# -*- coding: utf-8 -*-

"""
Driver for managing git repositories
"""

import os

import pygit2


def repo_clone(repo):
    """Clone repo or checkout last changes on branch

    :param repo: (Repository) object with
                 "url", "path" and "branch" attributes
    """

    # TODO: if exists
    if os.path.exists(repo.path):
        repo_path = pygit2.discover_repository(repo.path)
        repo_obj = pygit2.Repository(repo_path)
        repo_obj.remotes[0].fetch()
        repo_obj.checkout_head()
        return
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
