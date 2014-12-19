# -*- coding: utf-8 -*-

import os
import logging
import select
import shlex
import subprocess

LOG = logging.getLogger(__name__)


class cd(object):

    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def execute_cmd(command):
    p = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    while True:
        reads = [p.stdout.fileno(), p.stderr.fileno()]
        ret = select.select(reads, [], [])

        for fd in ret[0]:
            if fd == p.stdout.fileno():
                read = p.stdout.readline()
                LOG.debug('stdout: ' + read)
            if fd == p.stderr.fileno():
                read = p.stderr.readline()
                LOG.debug('stderr: ' + read)

        if p.poll() is not None:
            break
