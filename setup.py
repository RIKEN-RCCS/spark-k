#!/usr/bin/env python

import sys
import os
import shutil
from setuptools import setup

shutil.copyfile('scripts/spark-k-submit.py', 'scripts/spark-k-submit')
shutil.copyfile('scripts/spark-k-wait.py', 'scripts/spark-k-wait')

setup(
    name='spark-k',
    packages=[],
    version='1.0.0',
    scripts=[
        os.path.join('script', 'spark-k-submit'),
        os.path.join('script', 'spark-k-wait'),
        os.path.join('script', 'spark-k-initialize'),
        os.path.join('script', 'spark-k-finalize'),
        os.path.join('script', 'spark-k')],
    install_requires=[],
)
