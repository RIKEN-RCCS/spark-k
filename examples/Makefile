# Makefile

PERF = spark-perf-master
PERFFILES = $(PERF)/bin $(PERF)/lib
PERFFILES += $(PERF)/spark-tests/target/spark-perf-tests-assembly.jar
PERFFILES += $(PERF)/streaming-tests/target/streaming-perf-tests-assembly.jar
PERFFILES += $(PERF)/mllib-tests/target/mllib-perf-tests-assembly.jar
PERFFILES += $(PERF)/pyspark-tests/*.py

.PHONY: data-manipulation-downloads simpleapps \
	spark-perf-download spark-perf-build veryclean

data-manipulation-downloads::
	wget -O commons-csv-1.1.jar http://search.maven.org/remotecontent?filepath=org/apache/commons/commons-csv/1.1/commons-csv-1.1.jar
	wget -O spark-csv_2.11-1.0.3.jar http://search.maven.org/remotecontent?filepath=com/databricks/spark-csv_2.11/1.0.3/spark-csv_2.11-1.0.3.jar
	wget http://s3-us-west-2.amazonaws.com/sparkr-data/flights.csv

simpleapps::
	cd java; make
	cd scala; make

spark-perf-download::
	wget https://github.com/databricks/spark-perf/archive/master.zip
	unzip master.zip

spark-perf-build::
	python spark-perf-build.py

spark-perf.tz::
	tar zcf spark-perf.tz $(PERFFILES)

spark-perf-config.diff::
	diff -u spark-perf-master/config/config.py.template \
		spark-perf-config-basic.py > spark-perf-config.diff; true

veryclean::
	rm -f run??-*.sh.[eioswz][0-9]*
