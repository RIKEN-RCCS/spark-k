[](-*-Mode: Fundamental; Coding: us-ascii;-*-)

# Utility Scripts for Apache Spark on K

These scripts are utility to ease using Apache Spark on K.  The
scripts are installed in "/opt/aics/spark/scripts" on K.

## Install

Download scripts for K.

    $ git clone https://github.com/pf-aics-riken/spark-k

Copy the scripts on the compute-node (an interactive run).

    $ cd spark-k
    $ mkdir /opt/aics/spark/scripts
    $ cp -p scripts/* /opt/aics/spark/scripts

> Prepare Python package "setuptools".  The downloaded files are
installed in "${HOME}/.local/lib/python2.6/".
>    $ wget https://bootstrap.pypa.io/ez_setup.py -O - | python - --user

# (2016-07-20) MEMO on Environment Variables

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
