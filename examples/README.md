<!-- -*-Mode: Fundamental; Coding: us-ascii;-*- -->

# Examples of Spark on K (2016-07-21)

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

* Scripts "run2x-xxx.sh" run tests of Spark-Perf.  Spark-Perf is at
https://github.com/databricks/spark-perf.  Build is necessary.
"run20-spark-perf.sh" runs "SPARK_TESTS".
"run23-spark-perf-pearson.sh" runs only "PEARSON" from MLLIB.

* Scripts "run3x-xxx.sh" run tests Scala Pi (same as run00), but using
the "micro"-queue and without rank-directories.

## Notes on run03-r.sh

It runs "ml.R" and "dataframe.R".  Note "RSparkSQLExample.R" is not
included because it is missing while it appears in the recent source
tree.

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

Note SimpleApp in Python does not launch wokers.

## Notes on run20-spark-perf.sh

It runs "SPARK_TESTS".  It sets the number of nodes very small
(node=8).  Running with larger nodes fails due to limits of Java
memory or number of open files.

## Notes on run23-spark-perf-pearson.sh

It runs MLLIB "pearson".  "run23" runs with relatively large 384
workers, and "run24" with small workers (48, 96, 192).

Results are in
"run23-spark-perf-pearson.sh.wNNN/mllib_perf_output_XXX".  Note the
"Time:" line consists of (med, std, min, first-result, last-result).
See "spark-perf-master/lib/sparkperf/utils.py".

## Building Spark-Perf

Spark-Perf is at "https://github.com/databricks/spark-perf".  The used
version is commit 6e4f26de0fcd58b629abb8f5389bb15f914752e7 (Dec 9,
2015).

Download the package.

    $ make spark-perf-download

It downloads the package from
"https://github.com/databricks/spark-perf/archive/master.zip" and
unzips it.  The files will be expanded in "spark-perf-master".

Build.

    $ make spark-perf-build
    $ make spark-perf.tz

"spark-perf-build.py" is a modified copy of "lib/sparkperf/main.py".
All but build related routines are deleted.

The examples here uses a modified configuration file.  Additionally,
check the difference "spark-perf-config.basic.py".

    $ diff -u spark-perf-master/config/config.template.py ./spark-perf-config.basic.py

All tests are disabled in "spark-perf-config.basic.py".  It needs to
enable ones.

* RUN_SPARK_TESTS = True/False
* RUN_PYSPARK_TESTS = True/False
* RUN_STREAMING_TESTS = True/False
* RUN_MLLIB_TESTS = True/False
* RUN_PYTHON_MLLIB_TESTS = True/False

## Setting on spark-perf-config-basic.py

* The diff to the original is in "spark-perf-config.diff".

* Reduce "SCALE_FACTOR" from 1.0 to 0.1.  

* Reduce "spark.executor.cores" from 8 to 4.

* Comment out the option "spark.storage.memoryFraction", which is
deprecated.

Reducing "SCALE_FACTOR" and "spark.executor.cores", and using small
number of nodes is needed to run tests, which failed with
"java.lang.OutOfMemoryError" ("GC overhead limit exceeded" or "Java
heap space"), and "java.io.FileNotFoundException" ("Too many open
files").
