from setuptools import setup, find_packages
from distutils.command.sdist import sdist as sdist_orig
from distutils.errors import DistutilsExecError


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


class sdist(sdist_orig):

    def run(self):
        try:
            self.spawn(['sh', './scripts/initial_config.sh'])
        except DistutilsExecError:
            self.warn('Could not run config script, please run it using "sh ./scripts/initial_config.sh"')
        super().run()



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
    cmdclass={
        'sdist': sdist
    },


)
