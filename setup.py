#!/usr/bin/env python

import sys
import os
import shutil
from setuptools import setup

shutil.copyfile('scripts/spark-k-submit.py', 'scripts/spark-k-submit')
shutil.copyfile('scripts/spark-k-wait-initialize.py', 'scripts/spark-k-wait-initialize')
shutil.copyfile('scripts/spark-k-wait-spark-job-finish.py', 'scripts/spark-k-wait-spark-job-finish')

setup(
    name='spark-k',
    packages=[],
    version='1.0.0',
    scripts=[
        os.path.join('scripts', 'spark-k-submit'),
        os.path.join('scripts', 'spark-k-wait-initialize'),
        os.path.join('scripts', 'spark-k-wait-spark-job-finish'),
        os.path.join('scripts', 'spark-k-initialize'),
        os.path.join('scripts', 'spark-k-finalize'),
        os.path.join('scripts', 'spark-k')],
    install_requires=[],
)
