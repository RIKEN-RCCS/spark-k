# SimpleApp.py -*-Mode: Java; Coding: us-ascii;-*-
# Copyright The Apache Software Foundation.
# CODE TAKEN FROM http://spark.apache.org/docs/latest/quick-start.html

"""SimpleApp.py"""
from pyspark import SparkContext

logFile = "/opt/aics/spark/spark-1.6.2-bin-sparkk/README.md"
sc = SparkContext("local", "Simple App")
logData = sc.textFile(logFile).cache()

numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()

print("Lines with a: %i, lines with b: %i" % (numAs, numBs))
