from mpi4py import MPI
import numpy
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
numProcess = comm.Get_size()


main_msg = 1001
mesg_check = -1
mesg_am_alive = rank

##to transfer this message to all the processes 
##lets try to use some simple try and except by
##simply adding a code block before the send message.

for i in range(1,1000):

    for i in range(0,numProcess):
        if i != rank:
            try:
                comm.send(mesg_check,dest=i)
            except:
                print("Node doesnt exist")
                
        
    for i in range(0,numProcess):
        if i != rank:
            try:
                k = comm.recv(source=i)
#                print("sender = " ,i, "and receiver = ", rank)
            except:
                print("One Node Failed, but continuing execution")
        

    time.sleep(1.0)
    print("number of processes running are = ",numProcess)


MPI.Finalize()
