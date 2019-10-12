
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='dmas',
    version='1.0',
    packages=find_packages(),
    license='MIT',
    url='https://gitlab.com/nicofirst1/mas_traffic',
    include_package_data=True,
    author='Nicolo Brandizzi',
    install_requires=requirements,
    description='Project for Design of Multi-Agent Systems KIM.DMAS04.2019-2020.1A, University of GroningenOSM ',

)
