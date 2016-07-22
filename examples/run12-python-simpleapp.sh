#!/bin/sh -x

# Runs SimpleApp.py in a local source file.  The code of SimpleApp.py
# is taken from http://spark.apache.org/docs/latest/quick-start.html.
# It runs with 12 nodes (1 master + 12 workers), using
# "rank"-directory.

#PJM --rsc-list "rscgrp=small"
#PJM --rsc-list "node=12"
#PJM --rsc-list "elapse=00:03:00"
#PJM --mpi "use-rankdir"
#PJM -S
#PJM --stgin "rank=* python/SimpleApp.py %r:./"
#PJM --stgout "rank=* %r:./spark.logs/* ./%n.z%j/"
#PJM --stg-transfiles "all"

. /work/system/Env_base > /dev/null

k_scripts=/opt/aics/spark/scripts/
. ${k_scripts}/spark-k-config.sh
. ${k_scripts}/spark-k-functions.sh

spark_k_setup
spark_k_start_all

${SPARK_HOME}/bin/spark-submit \
    --master "${k_master_url}" \
    ./SimpleApp.py

spark_k_stop_all
spark_k_clean
