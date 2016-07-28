#!/bin/sh -x

# Runs PEARSON in MLLIB tests with 384 nodes.  Run
# run24-spark-perf-pearson.sh for small scale.

#PJM --rsc-list "rscgrp=large"
#PJM --rsc-list "node=396"
#PJM --rsc-list "elapse=00:20:00"
#PJM -S
#PJM --stgin "./spark-perf.tz ./"
#PJM --stgin "./spark-perf-config-common.py ./"
#PJM --stgout-dir "./results ./%n.w%j/ recursive=10"
#PJM --stgout "./perf-config.py ./%n.w%j/"
#PJM --stgout "./spark.logs/* ./%n.z%j/"
#PJM --stg-transfiles "all"

. /work/system/Env_base > /dev/null

cat spark-perf.tz | (cd ${PJM_JOBDIR}; tar zxf -)

sed -e 's/#TEST_SETS#/RUN_MLLIB_TESTS = True \
mllib_pearson = [("pearson", MLLIB_PERF_TEST_RUNNER, SCALE_FACTOR, \
    MLLIB_JAVA_OPTS, [ConstantOption("pearson")] + MLLIB_PEARSON_TEST_OPTS)] \
MLLIB_TESTS += mllib_pearson/' \
	<spark-perf-config-common.py >perf-config.py

k_scripts=/opt/aics/spark/scripts/
. ${k_scripts}/spark-k-config.sh
. ${k_scripts}/spark-k-functions.sh

spark_k_setup 384
spark_k_start_all

${PJM_JOBDIR}/spark-perf-master/bin/run --config perf-config.py

spark_k_stop_all
spark_k_clean

sleep 20
