# -*- coding: utf-8 -*-
#    Copyright 2014 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

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
