<!-- -*-Mode: Fundamental; Coding: us-ascii;-*- -->

# Running Spark on K
==================

## 1.  Introduction

The "spark-k" package is a utility for Spark running on K computer,
This document aims at Spark users of an ordinary clusters.

Compared to an ordinary cluster environment, K computer differs in
following characteristics:

* Jobs are under the control of a job-scheduler.

* The working storage is "staged".  The working set files must be
copied in from the permanent storage system to the working storage
system by "stage-in", and results must be copied out by "stage-out".

* Processes on the allocated node must be started by the "mpiexec"
command provided in MPI (Message Passing Interface).

## 2. Writing a Job Script

A job script is in the form a shell script (bash).  The user needs to
write the following steps in her job script:

1. Specify a request of the number of the nodes.

2. Specify the input files for stage-in.

3. Start a master.

4. Start workers.

5. Wait for all the workers are registered into the master.

6. Launch some jobs by spark-submit.

7. Wait for the jobs finish (not necessary normally).

8. Stop workers.

9. Stop the master.

10. Specify the output files for stage-out, maybe including logs.

```
#PJM --rsc-list "rscgrp=small"
#PJM --rsc-list "node=48"
#PJM --rsc-list "elapse=00:03:00"
#PJM --mpi "use-rankdir"
#PJM -S
#PJM --stgin "...omit..."
#PJM --stgout "...omit..."
#PJM --stg-transfiles "all"
...omit...
```

A written job script can be issued with the "pjsub" command:

```shell
$ pjsub your_job.sh
```

A job script is executed on the node rank=0.

## 3. File System Structure

There are two types of file systems are used, which are specific to K.

* "rank"-directories: Directory is only accessible from the node.

* "shared"-directories: Directory is on a network file system (Lustre
File System).

The use of rank-directories is recommended for performance.  The use
is specified by a job-script line:

```
#PJM --mpi "use-rankdir"
```

## 4. Stage-In Input Files

To put the input data for Spark applications in a K job,
you can specify stage-in options to "pjsub".

And to get the output data of Spark applications in a K job,
you can also specify stage-out options to "pjsub".

Input data for Spark applications would be put in the shared directory.

To stage the input files in, specify options like:

```shell
$ pjsub --stgin "rank=0 <path to the input file> ./../"  your_job.sh
```

or write the following line in the job script:

```
#PJM --stgin "rank=0 <path to the input file> ./../"
```

## 6. Stage-Out Output Files

Staging specifications to stage out the output files out:

```
#PJM --stgout "rank=* %r./filename ./somewhere/"
```

Log files of master/workers are created in the "logs" directory in
rank-directory on each node.  Specify the following line, to stage out
log files:

```
#PJM --stgout-dir "rank=* ./logs/ ./logs/ recursive=10"
```

Working files of executors are placed in the "work" directory.
Specify the following line, to stage out working files:

```
#PJM --stgout-dir "rank=* %r:./work/ ./work/ recursive=10"
```

Note "recursive=10" above is needed because it does not traverse
directories by default.

## 7. Example Job Scripts

See [examples](../examples).
