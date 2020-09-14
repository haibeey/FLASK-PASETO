from setuptools import find_packages, setup
import os 

import flask_paseto

basedir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name="Flask-PASETO",
    packages=find_packages(),
    version="0.0.4",
    include_package_data=True,
    description="Paseto integration for flask",
    author="Akerele Abraham",
    license="MIT",
    setup_requires=[
        "pytest-runner",
        "flask",
        "paseto>=0.0.5",
        "pysodium>=0.7.5"
    ],
    tests_require=["pytest"],
    package_data={"": ["*"]},
    test_suite="tests",
    url="https://github.com/haibeey/FLASK-PASETO",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "flask",
        "paseto>=0.0.5",
        "pysodium>=0.7.5"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',    
        'Intended Audience :: Developers',    
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3', 
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
  ],
)