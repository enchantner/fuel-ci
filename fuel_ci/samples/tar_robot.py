# -*- coding: utf-8 -*-

from fuel_ci import actions as act

from fuel_ci.flow.base import BaseFlow


class BuildRobot(BaseFlow):

    def __init__(self):
        super(BuildRobot, self).__init__()
        self.robots = self.artifact("robots")

    def _get_file(self):
        act.download(self.robots.url, self.robots.path)

    def _pack_file(self):
        act.pack_tar([self.robots.path], self.robots.archive)

    def prepare(self):
        self._get_file()

    def build(self):
        self._pack_file()

    def clean(self):
        act.delete_file(self.robots.path)


if __name__ == "__main__":
    BuildRobot().run()
