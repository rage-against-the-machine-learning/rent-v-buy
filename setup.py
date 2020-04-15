from setuptools import setup, find_packages
from os import path

setup (
    name = "rent-v-buy"
    , version = "0.1"
    , description = "Use Zillow Data to help determine if consumer should rent v. buy."
    , url = "https://github.com/rage-against-the-machine-learning/rent-v-buy"
    , author = "Team Tufte Love"
    , package_dir = {'':'src'}
    , packages = find_packages()
    , install_requires = [
        'numpy'
        , 'pandas'
        , 'sklearn'
        , 'json'
    ]
)
