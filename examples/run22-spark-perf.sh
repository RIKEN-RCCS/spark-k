#!/bin/sh -x

# Runs Spark-Perf with RUN_MLLIB_TESTS=True.  It will take a long time
# and only will finish a few tests.

#PJM --rsc-list "rscgrp=small"
#PJM --rsc-list "node=129"
#PJM --rsc-list "elapse=04:00:00"
#PJM -S
#PJM --stgin "./spark-perf.tz ./"
#PJM --stgin "./spark-perf-config-basic.py ./"
#PJM --stgout-dir "./results ./%n.w%j/ recursive=10"
#PJM --stgout "./perf-config.py ./%n.w%j/"
#PJM --stgout "./spark.logs/* ./%n.z%j/"
#PJM --stg-transfiles "all"

. /work/system/Env_base > /dev/null

cat spark-perf.tz | (cd ${PJM_JOBDIR}; tar zxf -)

sed -e 's/RUN_MLLIB_TESTS = False/RUN_MLLIB_TESTS = True/' \
	<spark-perf-config-basic.py >perf-config.py

k_scripts=/opt/aics/spark/scripts/
. ${k_scripts}/spark-k-config.sh
. ${k_scripts}/spark-k-functions.sh

spark_k_setup
spark_k_start_all

${PJM_JOBDIR}/spark-perf-master/bin/run --config perf-config.py

spark_k_stop_all
spark_k_clean
