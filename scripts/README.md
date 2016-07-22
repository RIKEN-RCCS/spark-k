;; -*-Mode: Fundamental; Coding: utf-8;-*-

Random memo.

*** (2016-07-20) Environment Variables

** SPARK_MASTER

${SPARK_MASTER} points to a master copy of Spark
installation.  Setting ${SPARK_MASTER} causes to make a copy (rsync)
from ${SPARK_MASTER} to ${SPARK_HOME} in "start-daemon.sh"

** SPARK_PID_DIR

${SPARK_PID_DIR} should not be shared among nodes.  "start-daemon.sh"
stores a PID in a file which probably has the same name:
"spark--$command-$instance.pid".

** SPARK_WORKER_MEMORY

${SPARK_WORKER_MEMORY} is set to memory size minus 1GB by default, but
it is too large for K on which swapping is disabled.
