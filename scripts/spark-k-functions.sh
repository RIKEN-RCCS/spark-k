#!/bin/bash

# Simple scripts for running Spark.  Source this file.

# (spark_k_setup) Generates a host-list file.  It determines the nodes
# for a master and workers, and generates a host-list file and a
# setting file.  Optional first argument limits the number of workers.
# A host-list consists of hostnames of worker nodes.  It assigns a
# single master and (nprocs-1) workers.  A master is on rank=0.  A
# setting file contains variables "${k_master_node}",
# "${k_master_url}", and "${k_n_workers}".  These variables are
# environment-exported to be accessible from subprocesses of Python,
# etc.  Note that the files are created in "${PJM_JOBDIR}", which
# points to a so-called "shared"-directory and accessible from all
# nodes.  Normally, a "shared"-directory is one up from a
# "rank"-directory.  This is called by the main job script (a single
# process).  As a by-product, it also generates another list
# consisting of all nodes.

spark_k_setup() {
    # Make a "conf" directory.

    mkdir -p ${k_conf_dir}

    # Make a host-list.

    if [ -n "$1" ] && [ "$1" -gt 0 ]; then
        nprocs=`expr "$1" + 1`
        mpiexec -n "$nprocs" ${k_scripts}/gatherhostnames "${k_nodes_file}"
    else
        mpiexec ${k_scripts}/gatherhostnames "${k_nodes_file}"
    fi

    # Determine the rank0 for a master and the rest for the workers.

    hostname=`hostname`
    export k_master_node="${hostname}"
    export k_master_url="spark://${k_master_node}:7077"

    grep -v -e "${k_master_node}" < ${k_nodes_file} > ${k_worker_nodes_file}

    k_n_nodes=`wc -l < ${k_nodes_file} 2> /dev/null`
    export k_n_workers=`wc -l < ${k_worker_nodes_file} 2> /dev/null`

    if [ "${k_n_workers}" -le 0 ]; then
        echo "warning: Number of workers 0." 1>&2
    fi

    # Generate settings file for the master/workers.

    cat <<EOF > ${k_settings_file}
#!/bin/bash
# Settings of a Spark run.  Source this file.
export k_master_node=${k_master_node}
export k_master_url=${k_master_url}
export k_n_workers=${k_n_workers}
EOF
}

# (spark_k_start_all) Starts Spark processes.  It starts a master and
# workers processes.  It waits until all processes are certainly
# started.  It is called by the main job script (a single process).

spark_k_start_all() {
    mpiexec /work/system/bin/msh ${k_scripts}/spark-k-start.sh
    ${k_scripts}/spark-k-wait-start.py ${k_n_workers} --host ${k_master_node}
}

# (spark_k_stop_all) Stops Spark processes.  It waits for finish of
# all Spark jobs and shuts down the master and the workers.  It is
# called by the main job script (a single process).

spark_k_stop_all() {
    ${k_scripts}/spark-k-wait-finish.py --host ${k_master_node}
    mpiexec /work/system/bin/msh ${k_scripts}/spark-k-stop.sh
}

# (spark_k_clean) Clean files.  Run this last.

spark_k_clean() {
    rm -f ${k_settings_file} ${k_nodes_file} ${k_worker_nodes_file}
}
