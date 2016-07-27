<!-- -*-Mode: Fundamental; Coding: us-ascii;-*- -->

# Using Apache Spark on K

This package provides installation documentation and utility scripts
for running [Apache Spark](http://spark.apache.org/) on [K
Computer](http://www.aics.riken.jp/en/k-computer/about/).  It also
includes simple examples.

* The installation documentation is in [docs](docs).  Spark (1.6.2) is
installed in "/opt/aics/spark/spark-1.6.2-bin-sparkk" on K.

* The utility scripts are in [scripts](scripts).  The scripts are in
"/opt/aics/spark/scripts" on K.

* The examples are in [examples](examples).  They are provided as job
scripts for Fujitsu job manager.

## Basics

The scripts are simple wrappers of the scripts of Spark, which help
start/stop master and worker processes.  Spark runs in the [Spark
standalone
mode](http://spark.apache.org/docs/latest/spark-standalone.html), but
master/workers are started using MPI (Message Passing Interface) via
mpiexec.

Check out that Spark is installed in "/opt/aics/spark" and R in
"/opt/aics/R" (on the compute-nodes).

## Running Examples

First try the sample job scripts (for Fujitsu job manager) in the
[examples](examples).

## Building Spark

For build and install procedures, see [docs](docs).

## More Information

* For more information using Spark on K, see [Basics in
docs](docs/BASICS.md).
