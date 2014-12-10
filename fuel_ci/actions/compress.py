# -*- coding: utf-8 -*-

import tarfile


def pack_tar(file_list, path):
    tar = tarfile.open(path, "w")
    for name in file_list:
        tar.add(name)
    tar.close()
