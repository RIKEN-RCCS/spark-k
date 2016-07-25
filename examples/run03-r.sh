#!/bin/sh -x

# Runs two R examples, with 12 nodes (1 master + 11 workers), using
# "rank"-directories.

#PJM --rsc-list "rscgrp=small"
#PJM --rsc-list "node=12"
#PJM --rsc-list "elapse=00:10:00"
#PJM --mpi "use-rankdir"
#PJM -S
#PJM --stgout "rank=0 0:../spark.conf/* ./%n.z%j/"
#PJM --stgout "rank=* %r:./spark.logs/* ./%n.z%j/"
#PJM --stg-transfiles "all"

. /work/system/Env_base > /dev/null

k_scripts=/opt/aics/spark/scripts/
. ${k_scripts}/spark-k-config.sh
. ${k_scripts}/spark-k-functions.sh

spark_k_setup
spark_k_start_all

(sleep 5; echo ""; echo "*** RUNNING ML.R... ***"; echo "")

${SPARK_HOME}/bin/sparkR \
    --master "${k_master_url}" \
    ${SPARK_HOME}/examples/src/main/r/ml.R

(sleep 5; echo ""; echo "*** RUNNING DATAFRAME.R... ***"; "echo "")

${SPARK_HOME}/bin/spark-submit \
    --master "${k_master_url}" \
    ${SPARK_HOME}/examples/src/main/r/dataframe.R

spark_k_stop_all
#spark_k_clean

sleep 20
