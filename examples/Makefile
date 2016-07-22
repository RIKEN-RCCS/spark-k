# Makefile

PERF = spark-perf-master
PERFFILES = $(PERF)/bin $(PERF)/lib
PERFFILES += $(PERF)/spark-tests/target/spark-perf-tests-assembly.jar
PERFFILES += $(PERF)/streaming-tests/target/streaming-perf-tests-assembly.jar
PERFFILES += $(PERF)/mllib-tests/target/mllib-perf-tests-assembly.jar
PERFFILES += $(PERF)/pyspark-tests/*.py

.PHONY: spark-perf-build

spark-perf-build::
	spark-perf-build.py

spark-perf.tz::
	tar zcf spark-perf.tz $(PERFFILES)

veryclean::
	mv run??-*.sh.[eioswz][0-9]* tmp/
	#rm -f run??-*.sh.[eioswz][0-9]*
