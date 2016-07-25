#!/bin/sh -x

# Runs data-manipulation.R in the examples, with 12 nodes (1 master +
# 11 workers), using "rank"-directories.  It needs to download files
# "flights.csv", "commons-csv-1.1.jar", and
# "spark-csv_2.11-1.0.3.jar".  See the Makefile.

#PJM --rsc-list "rscgrp=small"
#PJM --rsc-list "node=12"
#PJM --rsc-list "elapse=00:10:00"
#PJM --mpi "use-rankdir"
#PJM -S
#PJM --stgin "rank=0 ./flights.csv 0:../"
#PJM --stgin "rank=* ./commons-csv-1.1.jar %r:./"
#PJM --stgin "rank=* ./spark-csv_2.11-1.0.3.jar %r:./"
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
    --jars "commons-csv-1.1.jar,spark-csv_2.11-1.0.3.jar" \
    ${SPARK_HOME}/examples/src/main/r/data-manipulation.R ../flights.csv

spark_k_stop_all
spark_k_clean

sleep 20
