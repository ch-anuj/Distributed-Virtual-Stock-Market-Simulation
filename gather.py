from mpi4py import MPI
import random as rd
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
numProcess = comm.Get_size()

listData = []

if rank == 0:
    data = rd.randint(-100,100)
else:
    data = rd.randint(-100,100)

for i in range(0,numProcess-1):
    dataN = comm.bcast(data, root=i)
    listData.append(dataN)

print(listData)
