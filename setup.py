import subprocess

import setuptools.command.build_ext as _build_ext
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


class build_ext(_build_ext.build_ext):
    def run(self):
        command = ['./scripts/initial_config.sh']
        subprocess.check_call(command)


setup(
    name='dmas',
    version='1.0',
    packages=find_packages(),
    license='MIT',
    url='https://gitlab.com/nicofirst1/dmas',
    include_package_data=True,
    author='Dizzibus',
    install_requires=requirements,
    description='Project for Design of Multi-Agent Systems KIM.DMAS04.2019-2020.1A, University of GroningenOSM ',

)
