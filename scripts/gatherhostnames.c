/* gatherhostnames.c (2016-01-18) */

/* Gather and print processor names on rank0.  It is used to recover a
   host-list of the job (it returns only static processes). */

#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <limits.h>
#include <assert.h>

int
main(int argc, char *argv[])
{
    if (argc != 2) {
	fprintf(stderr, "Usage mpiexec -n N gatherhostnames filename\n");
	fflush(0);
	return 1;
    }

    MPI_Init(&argc, &argv);

    int nprocs, rank;
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    char name[MPI_MAX_PROCESSOR_NAME];
    char names[nprocs][MPI_MAX_PROCESSOR_NAME];
    int namelen;
    MPI_Get_processor_name(name, &namelen);
    name[MPI_MAX_PROCESSOR_NAME - 1] = 0;
    MPI_Gather(name, sizeof(name), MPI_CHAR,
               names, sizeof(name), MPI_CHAR,
               0, MPI_COMM_WORLD);
    if (rank == 0) {
	FILE * f = fopen(argv[1], "w");
	if (f == 0) {
	    int e = errno;
	    char b[80];
	    snprintf(b, sizeof(b), "fopen(%s)", argv[1]);
	    perror(b);
	    MPI_Abort(MPI_COMM_WORLD, 1);
	    return 1;
	} else {
	    for (int i = 0; i < nprocs; i++) {
		fprintf(f, "%s\n", names[i]);
	    }
	    fflush(f);
	    fclose(f);
	}
    }

    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();

    return 0;
}
