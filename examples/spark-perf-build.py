#!/usr/bin/env python

# This is a modified copy of "lib/sparkperf/main.py" in Spark-Perf.
# All but build routines are deleted.  It uses
# config-file="spark-perf-config.basic.py".

import argparse
import imp
import os
import logging
import sys

sys.path.insert(0, "./spark-perf-master/lib")

logger = logging.getLogger("sparkperf")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

from sparkperf.commands import *
from sparkperf.cluster import Cluster
from sparkperf.mesos_cluster import MesosCluster
from sparkperf.testsuites import *
from sparkperf.build import SparkBuildManager

parser = argparse.ArgumentParser(description='Run Spark performance tests. Before running, '
    'edit the supplied configuration file.')

parser.add_argument('--config-file', help='override default location of config file, must be a '
    'python file that ends in .py', default="spark-perf-config.basic.py")

parser.add_argument('--additional-make-distribution-args',
    help='additional arugments to pass to make-distribution.sh when building Spark', default="")

args = parser.parse_args()
assert args.config_file.endswith(".py"), "config filename must end with .py"

# Check if the config file exists.
assert os.path.isfile(args.config_file), ("Please create a config file called %s (you probably "
    "just want to copy and then modify %s/config/config.py.template)" %
    (args.config_file, PROJ_DIR))

print "Detected project directory: %s" % PROJ_DIR
# Import the configuration settings from the config file.
print "Loading configuration from %s" % args.config_file
with open(args.config_file) as cf:
    config = imp.load_source("config", "", cf)

print("Building perf tests...")

SparkTests.build()

StreamingTests.build()

MLlibTests.build(config.MLLIB_SPARK_VERSION)

print("Finished builds.")
