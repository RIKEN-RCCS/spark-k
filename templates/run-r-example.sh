#!/bin/sh

#PJM --rsc-list "node=48"
#PJM --rsc-list "elapse=00:30:00"
#PJM --rsc-list "rscgrp=small"
#PJM --mpi "use-rankdir"
#PJM -s

#PJM --stg-transfiles "all"

export PATH=<path to install spark-k>:${PATH}

. ${SPARK_K_PATH}/spark-k-initialize

${SPARK_HOME}/bin/sparkR \
    --master ${SPARK_MASTER} \
    ${SPARK_HOME}/examples/src/main/r/ml.R

. ${SPARK_K_PATH}/spark-k-finalize


