from setuptools import setup, find_packages
from distutils.command.sdist import sdist as sdist_orig
from distutils.errors import DistutilsExecError
import subprocess


with open('requirements.txt') as f:
    requirements = f.read().splitlines()




cmds=['sh', './scripts/initial_config.sh']
MyOut = subprocess.Popen(cmds,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
stdout,stderr = MyOut.communicate()
print(stdout)
print(stderr)

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
