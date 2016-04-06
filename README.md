spark-k
=======

## 1.  Introduction

spark-k is utilities for Spark running on K computer, helps ordinary Spark
cluster user to adapt Spark running on super computer specific environment.

This section is mainly for Spark users on dedicated cluster environment.

Compared to ordinary Spark cluster environment, super computers, including the K
computer, differs in following characteristics:

* All the nodes which consist an computing environment is temporarily allocated
  for a job. Users request # of nodes to use for a job at a time.

* Technically there is no persistent storage. Users must "stage in" the needed
  input files into specific locations (in many cases it is the current working
  directory of the job) and "stage out" the desired result files.

* The allocated nodes have a rank number, which is defined by the MPI manner. If
  a user request 32 nodes environment, all the nodes have its own unique rank
  number, 0 to 31. All the nodes are only specifiable/recognized by the rank
  number, not by hostname/IP address in the temporary node set.

If a user want to run a Spark job in such an environment, the user must write
the following steps into a job script:

1. Request to allocate desired # of the nodes with the environment specific
   manner/command to the resource management module.

2. "Stage in" input files with the environment specific manner/command.

3. Launch a Spark master.

4. Launch Spark workers.

5. Wait for all the workers are registered into the master.

6. Launch a Spark job by spark-submit.

7. Wait for the Spark job finish.

8. Stop all Spark workers.

9. Stop the Spark master.

10. "Stage out" the output files, logs, etc.

In the K computer, those functionalities are accessible by using pjsub and it's
scripting manners/notations.
`spark-k` provides functionalities to ease above 3. - 9. steps.

Even with `spark-k`, you still have to use the environment specific
resource allocation manner/commands and stage-in/out mechanism.
This section is mainly for Spark users on dedicated cluster environment.

### 1.1. How to write the job script

The job script is a shell script.
You can submit a K job written in a shell script with the `pjsub` command like:

```shell
$ pjsub --rsc-list "node=8" --rsc-list "rscgrp=small" your_job.sh
```

You can specify `pjsub` options in the job script like:

```
#PJM --rsc-list "node=8"
#PJM --rsc-list "rscgrp=small"
```

For more detail, see manual pages or help of `pjsub`.

#### 1.1.1. File system structure

you should consider there are two types of directories that are used in the job script:

* The rank number directory
* The shared directory

##### 1.1.1.1. The rank number directory

For `spark-k`, use the rank number directory by executing `pjsub` with
`--mpi "use-rankdir"` or write the following line in the job script:

```
#PJM --mpi "use-rankdir"
```

The rank number directory is accessible
only from the node.

Your job script starts in the rank number directory on the rank 0 node.

##### 1.1.1.2. The shared directory

The shared directory is a parent directory of the rank directory.

The shared directory is accessible from all the nodes.

A unique shared directory is prepared for each K job.

#### 1.1.2. Stage In/Out

To put the input data for Spark applications in a K job,
you can specify stage-in options to `pjsub`.

And to get the output data of Spark applications in a K job,
you can also specify stage-out options to `pjsub`.

##### 1.1.2.1. Input for Spark applications

Input data for Spark applications would be put in the shared directory.

To stage the input files in, specify options like:

```shell
$ pjsub --stgin "rank=0 <path to the input file> ./../"  your_job.sh
```

or write the following line in the job script:

```
#PJM --stgin "rank=0 <path to the input file> ./../"
```

##### 1.1.2.2. Output from Spark applications

In many cases, It is useful to put output files in the shared directory,
so make the application to emit to the shared directory.

To stage out the output files out, , specify options like:

```shell
$ pjsub --stgout-dir "rank=0 <path to the output directory> ./" your_job.sh
```

or write the following line in the job script:

```
#PJM --stgout-dir "rank=0 <path to the output directory> ./"
```

##### 1.1.2.3. Output from Spark master/worker

###### 1.1.2.3.1. Log files

Log files of Spark Master/Worker are created in the `logs` directory
in each rank number directory.

To stage these logs out, write the following line in the job script:

```
#PJM --stgout-dir "rank=* ./logs/ ./logs/ recursive=10"
```

###### 1.1.2.3.2. Working directory

The work directory of a Spark executor is the `work` directory
in each rank number directory.

To stage these working directory out,
write the following line in the job script:

```
#PJM --stgout-dir "rank=* ./work/ ./work/ recursive=10"
```

#### 1.1.3. spark-k

You can use the `spark-k` scripts like in the following job-script:

```shell
#!/bin/sh

#PJM --rsc-list "node=8"
#PJM --rsc-list "elapse=00:30:00"
#PJM --rsc-list "rscgrp=small"
#PJM --mpi "use-rankdir"

export PATH=<path to install spark-k>:${PATH}

. <path to install spark-k>/*spark-k-initialize*

${SPARK_HOME}/bin/spark-submit --master ${SPARK_MASTER} <other options> ...

. <path to install spark-k>/*spark-k-finalize*
```

For more examples, see the `templates` directory.

## 2. spark-k Usage

### 2.1. Primitive scripts

#### 2.1.1. spark-k-initialize

```shell
. <path to install>/spark-k-initialize
```

`spark-k-initialize` initializes a Spark environment in K,
and defines these shell variables:

* **NODE_NUMBER**   the number of K nodes
* **SPARK_HOME**    the Spark home directory in the K environment
* **K_MASTER_NODE** the node in which Spark master running (default: the rank 0 node)
* **SPARK_MASTER**  the spark url (i.e. **spark://${K_MASTER_NODE}:7077** )
* **COMMON_DIR**    the absolute path of the shared directory

You must use `source` to load this script,
or you cannot use these shell variables.

You can change behavior of this script by defining
the following shell variable before use this script:

* **SEPARATE_DRIVER_NODE** if this variable isn't empty,
  Spark master runs in the rank 1 node if the node exists

If you want to run either Spark driver or Spark master in a different node,
define `SEPARATE_DRIVER_NODE` and submit a Spark application with `--deploy-mode client`.

#### 2.1.2. spark-k-finalize

```shell
. <path to install>/spark-k-finalize
```

`spark-k-finalize` waits for all spark job finish,
then stops a Spark master and all Spark workers.

#### 2.1.3. spark-k-wait-initialize

```
usage: spark-k-wait-initialize [-h] [--host HOST] [--port PORT]
                               [--interval INTERVAL]
                               [--retry-max RETRY_MAX]
                               [--node-num NODE_NUM]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           specify the host of Spark master (default: localhost).
  --port PORT           specify the port of Spark master UI (default: 8080).
  --interval INTERVAL   wait INTERVAL seconds between check Spark master UI
                        (default: 3).
  --retry-max RETRY_MAX
                        stop after RETRYMAX times chekcing (default: 0). When
                        RETRYMAX is 0, never stop until initialization finish.
  --node-num NODE_NUM   wait NODENUM workers connected to Spark master
                        (default: 0).
```

`spark-k-wait-initialize` waits for Spark workers connect to the Spark master.
`spark-k-initialize` uses this script implicitly.

#### 2.1.4. spark-k-wait-spark-job-finish

```
usage: spark-k-wait-spark-job-finish [-h] [--host HOST] [--port PORT]
                                     [--interval INTERVAL]
                                     [--retrymax RETRYMAX]

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          specify the host of Spark master (default: localhost).
  --port PORT          specify the port of Spark master UI (default: 8080).
  --interval INTERVAL  wait INTERVAL seconds between check Spark master UI
                       (default: 3).
  --retrymax RETRYMAX  stop after RETRYMAX times chekcing (default: 0). When
                       RETRYMAX is 0, never stop until all spark jobs finish.
```

`spark-k-wait-spark-job-finish` waits for all Spark jobs finish.
`spark-k-finalize` uses this script implicitly.

### 2.2. Convenient scripts

#### 2.2.1. spark-k-submit

```
Usage: spark-k-submit [-h|--help] spark_arguments ...
    -h,--help    Show this help
```

`spark-k-submit` is a wrapper script for `spark-submit`.

```shell
spark-k-submit <other options>...
```

is the same as the following:

```shell
. <path to install>/spark-k-initialize

${SPARK_HOME}/bin/spark-submit --master ${SPARK_MASTER} <other options>...

. <path to install>/spark-k-finalize
```

`spark-k-submit` add or replace the **--master** option
for Spark on the K computer.

#### 2.2.2. spark-k

```
spark-k <command>...:
    --help|-?    show this help.
```

`spark-k` is wrapper for any command for Spark on the K computer.

```shell
spark-k <command> <option>...
```

is the same as the following:

```shell
. <path to install>/spark-k-initialize

<command> <option>...

. <path to install>/spark-k-finalize
```
