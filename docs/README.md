[](-*-Mode: Fundamental; Coding: us-ascii;-*-)

# Using Spark on K

## Basics

* This "spark-k" package provides utility scripts to ease running
[Apache Spark](http://spark.apache.org) on
[K](http://www.aics.riken.jp/en/k-computer/).  Spark runs in the
[Spark standalone
mode](http://spark.apache.org/docs/latest/spark-standalone.html), but
the master/workers are started using MPI (via mpiexec).  This package
provides simple wrappers for the start/stop scripts.

* Check out Spark installed in "/opt/aics/spark" and R in
"/opt/aics/R" (on the compute-nodes).

* Also check out the utility scripts in "/opt/aics/spark/scripts" (on
the compute-nodes).

* First try the sample job scripts (for Fujitsu job manager) in the "examples".

## Simple Runs

* Copy and run the sample job scripts in the "examples" directory.
* [Running Spark-Perf](RunSparkPerf)

## Build Procedures

Spark is installed in "/opt/aics/spark", and R is installed in
"/opt/aics/R". They are built with the following procedures.

Brief procedures:

* [Build R on K](BuildR2)
* [Build Spark on K](BuildSpark2)
* [Install Utility Scripts on K](InstallScripts)

Detailed procedures but in Japanese:

* [Build R on K](BuildR)
* [Install Spark on K](InstallSpark)

## More Information

* For more information, see [Basics](BASICS).
