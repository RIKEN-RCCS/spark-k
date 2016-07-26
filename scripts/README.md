[](-*-Mode: Fundamental; Coding: us-ascii;-*-)

# Utility Scripts for Apache Spark on K

These scripts are utility to ease using Apache Spark on K.  The
scripts are installed in "/opt/aics/spark/scripts" on K.  See
"https://github.com/pf-aics-riken/spark-k" for information.

## Install

The scripts should be installed by the maintainer.  But, it is
necessary when someone wants to use these scripts on other than K.

Download the scripts for K.

    $ git clone https://github.com/pf-aics-riken/spark-k

Compile gatherhostnames, it is written in C.

    $ cd spark-k
    $ make gatherhostnames

Copy the scripts on the compute-node (an interactive run).

    $ (interactive run)
    $ cd spark-k
    $ mkdir -p /opt/aics/spark/scripts
    $ make install

> Prepare Python package "setuptools".  The downloaded files are
installed in "${HOME}/.local/lib/python2.6/".
>    $ wget https://bootstrap.pypa.io/ez_setup.py -O - | python - --user

# MEMO on Environment Variables (2016-07-20)

* SPARK_MASTER

${SPARK_MASTER} points to a master copy of Spark
installation.  Setting ${SPARK_MASTER} causes to make a copy (rsync)
from ${SPARK_MASTER} to ${SPARK_HOME} in "start-daemon.sh"

* SPARK_PID_DIR

${SPARK_PID_DIR} should not be shared among nodes.  "start-daemon.sh"
stores a PID in a file which probably has the same name:
"spark--$command-$instance.pid".

* SPARK_WORKER_MEMORY

${SPARK_WORKER_MEMORY} is set to memory size minus 1GB by default, but
it is too large for K on which swapping is disabled.
