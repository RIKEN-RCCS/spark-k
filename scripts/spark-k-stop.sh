#!/bin/bash
#set -x

# (spark-k-stop.sh) Spark process stopper.  It is run by mpiexec and
# stops a process on each node.  Note the master and the workers are
# not disjoint.

# Set the common environment.

k_scripts=/opt/aics/spark/scripts
. ${k_scripts}/spark-k-config.sh
. ${k_settings_file}

hostname=`hostname`

if (grep "${hostname}" "${k_worker_nodes_file}" >/dev/null); then
    ${SPARK_HOME}/sbin/stop-slave.sh 1>&2
fi

if [ "${hostname}" = "${k_master_node}" ]; then
    ${SPARK_HOME}/sbin/stop-master.sh 1>&2
fi
