#!/bin/sh

#PJM --rsc-list "node=48"
#PJM --rsc-list "elapse=00:30:00"
#PJM --rsc-list "rscgrp=small"
#PJM --mpi "use-rankdir"
#PJM -s

#COMMENT_OUT#PJM --stgin "rank=0 ./spark-k-initialize 0:."
#COMMENT_OUT#PJM --stgin "rank=0 ./spark-k-finalize 0:."
#COMMENT_OUT#PJM --stgin "rank=0 ./spark-k-initialize 0:."
#COMMENT_OUT#PJM --stgin "rank=0 ./spark-k-initialize 0:."

#PJM --stg-transfiles "all"

SPARK_K_PATH=.

. ${SPARK_K_PATH}/spark-k-initialize

${SPARK_HOME}/bin/sparkR \
    --master ${SPARK_MASTER} \
    ${SPARK_HOME}/examples/src/main/r/ml.R

. ${SPARK_K_PATH}/spark-k-finalize


