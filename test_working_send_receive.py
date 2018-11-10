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
    data = {'key1' : [1,2, 3], 'key2' : ( 'abc', 'xyz')}
    comm.send(data,dest=1)
elif rank==1:
    data = comm.recv(source=0)
    data1 = {'key1' : [1,2,3]}
    comm.send(data1,dest=2)
elif rank==2:
    data = comm.recv(source=1)
else:
    data = {'key3' : [1],'key4' : ('acd', 'aba')}

print(rank,data)


MPI.Finalize()
