[](-*-Mode: Fundamental; Coding: us-ascii;-*-)

# Examples of Apache Spark on K (2016-07-21)

This directory includes simple examples.  It lists job-scheduler
scripts for K (Fujitsu Parallel-Navi).

* Scripts "run0x-xxx.sh" run the code included in the Spark
installation, some are mentioned at the bottom in the "Quick Start"
page (http://spark.apache.org/docs/latest/quick-start.html).  The code
are in the "Apache Spark Examples" page
(http://spark.apache.org/examples.html).

* Scripts "run1x-xxx.sh" run the code shipped from this directory.
The codes are "SimpleApp" in the "Self-Contained Applications" section
in the "Quick Start" page
(http://spark.apache.org/docs/latest/quick-start.html).  The codes are
in directories "java", "python", and "scala".  Build is necessary, but
pre-compiled code is included.

* Scripts "run2x-xxx.sh" run tests of Spark-Perf.  Build is necessary.

## Notes on run03-r.sh

It runs "ml.R" and "dataframe.R".

Note "RSparkSQLExample.R" is not included, because it is missing while
it appears in the recent source tree.

## Notes on run04-r-data-manipulation.sh

Running "data-manipulation.R" needs some files to be downloaded.  Run
"make data-manipulation-downloads" for them.

* "flights.csv" from http://s3-us-west-2.amazonaws.com/.
* "commons-csv-1.1.jar" from http://search.maven.org/.
* "spark-csv_2.11-1.0.3.jar" from http://search.maven.org/.

It generates a warning: "WARN TaskSetManager: Stage 0 contains a task
of very large size (648 KB). The maximum recommended task size is 100
KB".

## Notes on run10-simpleapp.sh

Build procedures: The following run MVN for Java and SBT for Scala.

* cd java; make
* cd scala; make

Note SimpleAPp in Python does not launch wokers.

## Building Spark-Perf

Download the package.

    $ make spark-perf-download

It download the package
"https://github.com/databricks/spark-perf/archive/master.zip" and
unzips it.  The Files are expanded in "spark-perf-master".

Check a modified config file "spark-perf-config.basic.py".

    $ diff -u spark-perf-master/config/config.template.py ./spark-perf-config.basic.py

Build.

    $ make spark-perf-build
    $ make spark-perf.tz

"spark-perf-build.py" is a modified copy of "lib/sparkperf/main.py".
All but build related routines are deleted.

All tests are disabled in "spark-perf-config.basic.py".  Enable needed
ones.

* RUN_SPARK_TESTS = True/False
* RUN_PYSPARK_TESTS = True/False
* RUN_STREAMING_TESTS = True/False
* RUN_MLLIB_TESTS = True/False
* RUN_PYTHON_MLLIB_TESTS = True/False

## spark-perf "SPARK_TESTS"

* Reduce "SCALE_FACTOR" from 1.0 to 0.5.  It allows to run
"scala-agg-by-key" failed with "java.lang.OutOfMemoryError: GC
overhead limit exceeded".

* Set nprocs=12.  Reduce "num-partitions" and "reduce-tasks" from 400
to 100.  "scala-agg-by-key-naive" failed with
"java.io.FileNotFoundException: (Too many open files)"

NUM_PARTITIONS for "num-partitions"

## Notes on spark-perf-config-basic.py

* Option "spark.storage.memoryFraction" is said to be deprecated.
