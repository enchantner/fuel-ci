# -*- coding: utf-8 -*-

import requests


def download_artifact(artifact):
    r = requests.get(artifact.url, stream=True)
    if r.status_code == 200:
        with open(artifact.path, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
