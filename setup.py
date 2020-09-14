from setuptools import find_packages, setup
import os 

import flask_paseto

basedir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name="Flask-PASETO",
    packages=find_packages(),
    version="0.0.1",
    include_package_data=True,
    description="Paseto integration for flask",
    author="Akerele Abraham",
    license="MIT",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    package_data={"": ["*"]},
    test_suite="tests",
    long_description=long_description,
    long_description_content_type='text/markdown'
)