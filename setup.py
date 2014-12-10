# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


name = 'fuel-ci'
version = '0.0.1'


if __name__ == "__main__":
    setup(
        name=name,
        version=version,
        description='Fuel CI Build System',
        classifiers=[
            "Programming Language :: Python",
            "Topic :: Internet :: WWW/HTTP",
        ],
        packages=find_packages(),
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'fci = fuelclient.cli:main',
            ],
        }
    )
