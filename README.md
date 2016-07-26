[](-*-Mode: Fundamental; Coding: us-ascii;-*-)

# Using Apache Spark on K

This package provides installation documentation and utility scripts
for running [Apache Spark](http://spark.apache.org/) on [K
Computer](http://www.aics.riken.jp/en/k-computer/about/).  It also
includes simple examples.

* The installation documentation is in docs.  See [README in
docs](docs/README.md).

* The utility scripts are in scripts.  See [README in
scripts](scripts/README.md).

* The examples are provided as job scripts for Fujitsu job manager.
They are in examples.  See [README in examples](examples/README.md)

It assumes Spark is already installed in
"/opt/aics/spark/spark-1.6.2-bin-sparkk" and the scripts are in
"/opt/aics/spark/scripts".

## Basics

The scripts are simple wrappers of the scripts of Spark, which help
start/stop master and worker processes.  Spark runs in the [Spark
standalone
mode](http://spark.apache.org/docs/latest/spark-standalone.html), but
the master/workers are started using MPI (Message Passing Interface)
via mpiexec.

Check out that Spark is installed in "/opt/aics/spark" and R in
"/opt/aics/R" (on the compute-nodes).

## Running Examples

First try the sample job scripts (for Fujitsu job manager) in the
"examples".

* Run the sample job scripts in the "examples" directory.
* See [Running Spark-Perf](RunSparkPerf)

## Building Spark

For build and install procedures, see [README in
docs](docs/README.md).  Also, see
[wiki](https://github.com/pf-aics-riken/spark-k/wiki).

## More Information

* For more information, see [Basics in docs](docs/BASICS.md).
