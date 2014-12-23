# -*- coding: utf-8 -*-

"""
"""


def checkout(state):
    list(
        map(lambda r: r.clone(), state["objects"]["repositories"])
    )
    return state
