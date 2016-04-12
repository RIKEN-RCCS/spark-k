#!/bin/sh

#PJM --rsc-list "node=48"
#PJM --rsc-list "elapse=00:30:00"
#PJM --rsc-list "rscgrp=small"
#PJM --mpi "use-rankdir"
#PJM -s

#PJM --stg-transfiles "all"

export PATH=<path to install spark-k>:${PATH}

. ${SPARK_K_PATH}/spark-k-initialize

${SPARK_HOME}/bin/spark-submit \
    --master ${SPARK_MASTER} \
    --class org.apache.spark.examples.SparkPi \
    ${SPARK_HOME}/lib/spark-examples-1.6.0-hadoop2.2.0.jar

. ${SPARK_K_PATH}/spark-k-finalize
