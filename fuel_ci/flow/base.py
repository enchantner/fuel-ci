# -*- coding: utf-8 -*-

import argparse
import os

import yaml


class BaseFlow(object):

    config_file = None

    def __init__(self):
        self.parse_args()

        self.artifacts = {}

        with open(self.config_file, "r") as conf:
            config = yaml.load(conf.read())
        if 'artifacts' in config:
            self.artifacts = config['artifacts']

    def artifact(self, name):
        if name in self.artifacts:
            return type(name, (object,), self.artifacts[name])
        raise Exception("artifact '{0}' not found in config")

    def parse_args(self):
        self.parser = argparse.ArgumentParser()
        params, args = self.parser.parse_known_args()
        if not args:
            raise Exception("config file not specified")
        self.config_file = args[0]
        if not os.path.exists(self.config_file):
            raise Exception(
                "config file '{0}' does not exist".format(self.config_file)
            )

    def prepare(self):
        pass

    def build(self):
        pass

    def test(self):
        pass

    def publish(self):
        pass

    def clean(self):
        pass

    def run(self):
        self.prepare()
        self.build()
        self.test()
        self.publish()
        self.clean()
