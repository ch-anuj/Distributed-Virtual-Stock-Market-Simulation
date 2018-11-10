
import sys
import time
import mpi4py.MPI
mpi_comm = mpi4py.MPI.COMM_WORLD


def mpiabort_excepthook(type, value, traceback):
    mpi_comm.Abort()
    sys.__excepthook__(type, value, traceback)

def main():
    if mpi_comm.rank == 0:
        raise ValueError('Failure')

    print('{} continuing to execute'.format(mpi_comm.rank))
    time.sleep(1.0)
    print('{} exiting'.format(mpi_comm.rank))

if __name__ == "__main__":
    sys.excepthook = mpiabort_excepthook
    main()
    sys.excepthook = sys.__excepthook__
