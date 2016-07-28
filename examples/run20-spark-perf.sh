#!/bin/sh -x

# Runs Spark-Perf with RUN_SPARK_TESTS=True.  It runs with a very
# small setting with 8 nodes and 4 cores.  Larger setting may fail due
# to resource limits.

#PJM --rsc-list "rscgrp=small"
#PJM --rsc-list "node=8"
#PJM --rsc-list "elapse=0:40:00"
#PJM -S
#PJM --stgin "./spark-perf.tz ./"
#PJM --stgin "./spark-perf-config-basic.py ./"
#PJM --stgout-dir "./results ./%n.w%j/ recursive=10"
#PJM --stgout "./perf-config.py ./%n.w%j/"
#PJM --stgout "./spark.logs/* ./%n.z%j/"
#PJM --stg-transfiles "all"

. /work/system/Env_base > /dev/null

cat spark-perf.tz | (cd ${PJM_JOBDIR}; tar zxf -)

sed -e 's/RUN_SPARK_TESTS = False/RUN_SPARK_TESTS = True/' \
	<spark-perf-config-basic.py >perf-config.py

k_scripts=/opt/aics/spark/scripts/
. ${k_scripts}/spark-k-config.sh
. ${k_scripts}/spark-k-functions.sh

spark_k_setup
spark_k_start_all

${PJM_JOBDIR}/spark-perf-master/bin/run --config perf-config.py

spark_k_stop_all
spark_k_clean

sleep 20
