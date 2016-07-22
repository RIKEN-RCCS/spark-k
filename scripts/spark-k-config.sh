#!/bin/bash

# (spark-k-config.sh) Set of common environments.  Source this file.

# Unset "POSIXLY_CORRECT", which is (intentionally) exported on K.
# But the scripts of Spark fails when it is set.

unset POSIXLY_CORRECT

# Spark configuration.

export SPARK_HOME=/opt/aics/spark/spark-1.6.2-bin-sparkk

#(export SPARK_MASTER_PORT=7077)
export SPARK_CONF_DIR=${SPARK_CONF_DIR:-"${PJM_JOBDIR}/spark.conf"}
export SPARK_LOCAL_DIRS=${SPARK_LOCAL_DIRS:-'./spark.work'}
export SPARK_WORKER_DIR=${SPARK_WORKER_DIR:-'./spark.work'}
export SPARK_WORKER_MEMORY=${SPARK_WORKER_MEMORY:-'10G'}
export SPARK_LOG_DIR=${SPARK_LOG_DIR:-'./spark.logs'}
#export SPARK_DAEMON_MEMORY=${SPARK_DAEMON_MEMORY:-'1G'}
#export SPARK_PID_DIR=${SPARK_PID_DIR:-'/tmp'}

# Java configuration.

export JAVA_HOME=/opt/klocal/openjdk7u45
export PATH=${JAVA_HOME}/bin:$PATH
export CLASSPATH=.:${JAVA_HOME}/jre/lib:${JAVA_HOME}/lib:${JAVA_HOME}/lib/tools.jar

# Python configuration.

export PYTHON_HOME=/opt/local/Python-2.7.3
export PATH=${PYTHON_HOME}/bin:${PATH}
export LD_LIBRARY_PATH=${PYTHON_HOME}/lib:${LD_LIBRARY_PATH}

# R configuration.

#export R_HOME=/opt/aics/R
k_r_home=/opt/aics/R
export PATH=${k_r_home}/bin:$PATH

# Setting files for a job.

k_conf_dir=${SPARK_CONF_DIR}
k_settings_file=${SPARK_CONF_DIR}/spark_k_settings.${PJM_JOBID}
k_nodes_file=${SPARK_CONF_DIR}/spark_k_nodes.${PJM_JOBID}
k_worker_nodes_file=${SPARK_CONF_DIR}/spark_k_worker_nodes.${PJM_JOBID}
