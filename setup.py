from setuptools import setup

setup(
    name="offsec-python",
    version="0.0.1",    
    description="A watchdogs python library",
    author="WatchDogOblivion",
    license="BSD 2-clause",
    packages=["watchdogs"],
    install_requires=[
        "requests>=2.7",
        "beautifulsoup4>=2.7",                     
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",  
        "Operating System :: POSIX :: Linux",        
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)

"""
watchdogs.

A Watchdogs python library.
"""

__version__ = "0.0.1"
__author__ = "WatchDogOblivion"
__credits__ = "WatchDogs"