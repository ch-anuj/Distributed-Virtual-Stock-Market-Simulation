from mpi4py import MPI
import numpy as np
import random


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
numProcess = comm.Get_size()

clientsList = []
clientsPerRank = 3


if rank == 0:
    print('Entering the 0th processes')
    data_comp = {
                'c1' : {'mp': '12',
                        'ask': '13',
                        'bid': '11'},
                'c1' : {'mp': '23',
                        'ask': '24',
                        'bid': '21'}
                }
    comm.send(data_comp,dest=rank+1)
elif rank+1 < numProcess:
    data_comp = comm.recv(source=rank-1)
    comm.send(data_comp,dest=rank+1)
elif rank+1 == numProcess:
    data_comp = comm.recv(source=rank-1)
    circle

print(rank,data_comp)


MPI.Finalize()
