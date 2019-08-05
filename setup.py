from distutils.core import setup

setup(
    name='pylib',
    version='0.1.0',
    author='Zach Woods',
    packages=['pylib', 'pylib.test'],
    description='A library for python',
    long_description=open('README.md').read(),
    install_requires=[],
)