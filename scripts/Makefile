# Makefile (scripts)

gatherhostnames: gatherhostnames.c
	mpifccpx -o gatherhostnames gatherhostnames.c

FILES = spark-k-config.sh spark-k-functions.sh
FILES += spark-k-start.sh spark-k-stop.sh 
FILES += spark-k-wait-start.py spark-k-wait-finish.py
FILES += gatherhostnames 
FILES += gatherhostnames 

install:
	cp -p $(FILES) /opt/aics/spark/scripts/
