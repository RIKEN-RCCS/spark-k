<!-- -*-Mode: Fundamental; Coding: us-ascii;-*- -->

# Build R

## Note

* R is installed in "/opt/aics/R" on the compute-nodes.  This
procedure describes how it is built.

* The build is run on a compute-node (an interactive run).

This is a brief procedure; See the old procedure [BuildR](BuildR) for
details.

## Build R

Download.

    $ wget https://cran.r-project.org/src/base/R-3/R-3.2.3.tar.gz
    $ tar zxf R-3.2.3.tar.gz

Patch "src/library/tools/src/md5.c". The patch fixes alignment issue
(bus-error) to run on SPARC.

    @@ -70,11 +70,12 @@
     static void *
     md5_read_ctx (const struct md5_ctx *ctx, void *resbuf)
     {
    -  ((md5_uint32 *) resbuf)[0] = SWAP (ctx->A);
    -  ((md5_uint32 *) resbuf)[1] = SWAP (ctx->B);
    -  ((md5_uint32 *) resbuf)[2] = SWAP (ctx->C);
    -  ((md5_uint32 *) resbuf)[3] = SWAP (ctx->D);
    -
    +  md5_uint32 b[4];
    +  b[0] = SWAP (ctx->A);
    +  b[1] = SWAP (ctx->B);
    +  b[2] = SWAP (ctx->C);
    +  b[3] = SWAP (ctx->D);
    +  memcpy(resbuf, b, sizeof(b));
       return resbuf;
     }

Build (compile as an interactive run on a compute-node).

    $ . /work/system/Env_base
    $ export _JAVA_OPTIONS="-Xmx1g"
    $ export LIBRARY_PATH=${LD_LIBRARY_PATH}
    $ ./configure --prefix=/opt/aics/R --build=sparc64-unknown-linux-gnu --with-x=no CFLAGS=-O2 CXXFLAGS=-O2 FCFLAGS=-O2 FPICFLAGS=-KPIC FLIBS="-L/opt/FJSVtclang/GM-1.2.0-19/lib64 -lfj90f -lfj90i -lelf"
    $ make
    $ make check
    $ make install

The build will take about 40 minutes.
