# -*- coding: utf-8 -*-

import os
import fnmatch

from setuptools import setup
from pip.req import parse_requirements
from Cython.Build import cythonize


reqs = [str(r.req)
        for r in parse_requirements('requirements.txt', session=False)]

pyx_files = list()
for dirpath, dirnames, files in os.walk('./app'):
    for file in fnmatch.filter(files, '*.pyx'):
        pyx_files.append(os.path.join(dirpath, file))
pyx_extensions = cythonize(pyx_files)


setup(
    name='2L',
    version='0.0.1',
    description='2L, There is a surprise!',
    long_description='2L, SB! BIG S! BIG B! BIG SB!!!',
    url='https://github.com/Damnever/2L',
    author='Damnever',
    author_emial='dxc.wolf@gmail.com',
    license='The BSD 3-Clause License',
    keywords='bbs, forum, 2L',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    install_requires=reqs,
    ext_modules=pyx_extensions,
    entry_points={
        'console_scripts': [
            '2L=app.commands:main',
        ]
    },
)
