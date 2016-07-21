#!/bin/bash
#set -x

# (spark-k-start.sh) Spark process starter.  It is run by mpiexec and
# starts a process on each node.  Note the master and the workers are
# not disjoint.

# Set the common environment.

k_scripts=/opt/aics/spark/scripts
. ${k_scripts}/spark-k-config.sh
. ${k_settings_file}

hostname=`hostname`

if [ "${hostname}" = "${k_master_node}" ]; then
    ${SPARK_HOME}/sbin/start-master.sh 1>&2
fi

if (grep "${hostname}" "${k_worker_nodes_file}" >/dev/null); then
    ${SPARK_HOME}/sbin/start-slave.sh ${k_master_url} 1>&2
fi
