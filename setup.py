# -*- coding: utf-8 -*-

#     Copyright phmMS

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = "1.0"

setup(
    version=VERSION,
    name="phmMS",
    author="phmMS",
    author_email="phmms@beidouapp.com",
    license="",
    description="phmMS.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.5",
    packages=[
        'app',
        'app.models',
        'app.mqtt',
        'app.routers',
        'app.schemas',
        'app.schemas.schedule',
        'app.schemas.vrla',
        'app.services',
        'app.services.convert',
        'app.services.schedule',
        'app.utils',
        'phmconfig',
        'physics',
        'physics.transport',
        'physics.vrla',
        'physics.test',
        'physics.common',
        'physics.math'
    ],
    install_requires=[
        'blinker',
        'pytest',
        'setuptools',
        'imutils',
        'matplotlib',
        'requests',
        'fastapi',
        'uvicorn',
        'paho-mqtt',
        'pydantic',
        'aiofiles',
        'python-multipart',
        'fastapi-utils',
        'starlette',
        'loguru',
        'SQLAlchemy',
        'httpx',
        'numpy',
        'scipy',
        'pymysql',
        'pandas',
        'hdbscan',
        'sklearn',
        'scikit-learn',
        'adjustText',
        'statsmodels'
    ],
    download_url='',
    package_data={
        "*": ["tests/*"]
    })
