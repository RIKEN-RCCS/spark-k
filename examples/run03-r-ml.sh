#!/bin/sh -x

# Runs ml.R in the examples, with 12 nodes (1 master + 12 workers),
# using "rank"-directory.

#PJM --rsc-list "rscgrp=small"
#PJM --rsc-list "node=12"
#PJM --rsc-list "elapse=00:10:00"
#PJM --mpi "use-rankdir"
#PJM -S
#PJM --stgout "./spark.conf/* ./%n.z%j/"
#PJM --stgout "rank=* %r:./spark.logs/* ./%n.z%j/"
#PJM --stg-transfiles "all"

. /work/system/Env_base > /dev/null

k_scripts=/opt/aics/spark/scripts/
. ${k_scripts}/spark-k-config.sh
. ${k_scripts}/spark-k-functions.sh

spark_k_setup
spark_k_start_all

${SPARK_HOME}/bin/sparkR \
    --master "${k_master_url}" \
    ${SPARK_HOME}/examples/src/main/r/ml.R

spark_k_stop_all
