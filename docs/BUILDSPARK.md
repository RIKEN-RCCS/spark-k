<!-- -*-Mode: Fundamental; Coding: us-ascii;-*- -->

# Spark on K Build Procedure -- Update (2016-07-17)

## Note

* Apache Spark is installed in "/opt/aics/spark" on the compute-nodes.
  This describes how it is built.

* Build is run on a frontend.  Almost no cross compiling is necessary
as it is a JVM application.  The only exception is Snappy-Java, which
includes a binary library.

* Run this procedure on a frontend which is not too busy.  Most hosts
are too busy (insufficient memory) to run Java JVM.

This is a procedure for Spark 1.6.2.

## 1. (prerequisite) Maven

Maven is used in building Spark.

Clear existing Maven settings.

    $ cd ${HOME}
    $ rm -r .m2

Download (Use 3.3.9 now).

    $ wget ftp://ftp.riken.jp/net/apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz
    $ tar zxf apache-maven-3.3.9-bin.tar.gz

## 2. (prerequisite) Set paths and environments

    $ maven=...somewhere.../apache-maven-3.3.9
    $ export PATH=${maven}/bin:/opt/aics/R/bin:$PATH
    $ export JAVA_TOOL_OPTIONS="-Xmx2g -XX:ParallelGCThreads=1"

## 3. Snappy-Java

Snappy (and its Java binding) is a data-marshaller used in Spark.  A
distribution of Snappy includes binaries for many OS/processors
combinations but lacks for Linux/SPARCV9, and it is necessary to
cross-compile it.

Set fakes for cross-compiling by Fujitsu fcc/FCC compilers.

    $ cat > ~/bin/sparc64-unknown-linux-gnu-gcc <<EOF
    #!/bin/ksh
    fccpx -Xg $*
    EOF
    $ chmod +x ~/bin/sparc64-unknown-linux-gnu-gcc
    $ cat > ~/bin/sparc64-unknown-linux-gnu-g++ <<EOF
    #!/bin/ksh
    FCCpx -Xg $*
    EOF
    $ chmod +x ~/bin/sparc64-unknown-linux-gnu-g++

Download and patch Snappy-Java.  Use the version that matches Spark.
The version number can be found by grepping "snappy" in the "pom.xml"
in the top directory in the Spark source.

    $ git clone https://github.com/xerial/snappy-java.git
    $ cd snappy-java
    $ git checkout 1.1.2.1 -b 1.1.2.1
    $ git reset HEAD --hard
    $ wget https://raw.githubusercontent.com/pf-aics-riken/spark-k/master/snappy-java.patch.txt
    $ git apply -v snappy-java.patch.txt

The patch changes the Makefile for a library for "Linux" and
"sparcv9".  It also fixes the necessary version of the Snappy source.

Edit the version file to fake the version is "1.1.2.1".

    $ vi ./src/main/resources/org/xerial/snappy/VERSION

Build Snappy-Java.  Run make.  It downloads the Snappy source.  It
creates a package: "./target/snappy-java-1.1.2.1.jar".

    $ make

Register Snappy-Java in the Maven repository.  Run Maven at the
directory where the target file is visible:
"target/snappy-java-1.1.2.jar")

    $ mvn install:install-file -Dfile=target/snappy-java-1.1.2.1.jar -DgroupId=org.xerial.snappy -DartifactId=snappy-java -Dversion=1.1.2.1 -Dpackaging=jar -DgeneratePom=true

> (2016-07-21) The version of snappy used in this build is not the
latest, but one specified in the patch.  It needs to be changed from
-O2 to -O of the optimization option.  It hits an assertion error when
compiled with -O2.

## 4. Apache Spark

Download (Use 1.6.2 now).

    $ wget http://ftp.riken.jp/net/apache/spark/spark-1.6.2/spark-1.6.2.tgz
    $ tar zxf spark-1.6.2.tgz

Apply a patch (use git-apply although it is not a git file).  The
patch fixes an alignment issue (bus-error) to run on SPARC.

    $ cd spark-1.6.2
    $ wget https://raw.githubusercontent.com/pf-aics-riken/spark-k/master/spark.patch.txt
    $ git apply -v spark.patch.txt

Build Spark.

    $ ./build/mvn
    ## (Ignore errors from Maven: "[ERROR] No goals have been specified for this build. ...")

    ($ ./build/zinc-0.3.5.3/bin/zinc -shutdown)
    ($ ./build/mvn -DskipTests clean)
    $ ./make-distribution.sh --name sparkk --tgz -Psparkr
    $ ./build/zinc-0.3.5.3/bin/zinc -shutdown

It will take long time about an hour with a lot of downloading.

Check if Snappy-Java is packaged properly (the one compiled abobe is
actually in the package).  The binary "native/Linux/sparcv9" is not
included in the original distribution of Snappy-Java.

    $ jar tvf dist/lib/spark-assembly-1.6.2-hadoop2.2.0.jar | grep sparcv9
    |     0 Tue Jul 19 16:13:06 JST 2016 org/xerial/snappy/native/Linux/sparcv9/
    |113760 Tue Jul 19 16:13:06 JST 2016 org/xerial/snappy/native/Linux/sparcv9/libsnappyjava.so

Copy the package; run on a compute-node (an interactive run).

    $ cp -p spark-1.6.2-bin-sparkk.tgz /opt/aics/spark
    $ cd /opt/aics/spark
    $ tar zxf spark-1.6.2-bin-sparkk.tgz
    $ ln -s spark-1.6.2-bin-sparkk spark-1.6.0-bin-sparkk
