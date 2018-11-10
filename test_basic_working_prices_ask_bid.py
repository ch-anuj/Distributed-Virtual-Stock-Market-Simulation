from mpi4py import MPI
import numpy as np
import random as rd

# import logger
#
# logging.basicConfig(filename = "/home/anujc/Desktop/DstSysFIles/Project/VSMG/mpi4py/LOG_test_py.log",level = logging.DEBUG)
# logger = logging.getLogger()
#
# logger.info("intialising logging: 1st message")

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
numProcess = comm.Get_size()
currP = 100
clientsList = []
clientsPerRank = 3
bidList = []
askList = []
matchList = []
def constBid():
    for x in range(20):
        var = rd.randint(-100,100)
        var = var/75
        var = float("{0:.2f}".format(var))
        bidList.append(var)
        bidList.sort()

def constAsk():
    for x in range(20):
        var = rd.randint(-100,100)
        var = var/75
        var = float("{0:.2f}".format(var))
        askList.append(var)
        askList.sort()
# ask
def supply():
    var = 0
    for key in askList:
        var = var + key
    print("ask average = ",var)
#  bid
def demand():
    var = 0
    for key in bidList:
        var = var + key
    print("bid average = ",var)


def getMatchOrder():
    matchList = list(set(askList).intersection(bidList))
    list2 = []
    for k in matchList:
        list2.append(currP + k)
    print("last trade happend at these prices = " ,list2)

def newMarketP():
    var = 0
    np = currP
    if len(matchList) == 0:
        nP = currP
    else:
        for k in matchList:
            var = var + k
        lenMatch = len(matchList)
        nP = 0
    print("SE and new prices = (SE, prices) ", rank,np)

if rank == 0:
    # print('Entering the 0th processes')
    data_comp = {
                'c1' : {'mp': '12',
                        'ask': '13',
                        'bid': '11'}
                }
    for i in range(1,numProcess):
        comm.send(data_comp,dest=i)
    # for i in range(1,numProcess):
    #     from_se = comm.recv(source=i)
    constAsk()
    constBid()
    supply()
    demand()
    getMatchOrder()
    newMarketP()
    print('seperator ',rank)
    # print(bidList)
    # print(askList)

else:
    data_comp = comm.recv(source=0)
    # def buy(data_comp):
    #     for comp in data_comp:
    #         k = data_comp[comp]
    #         for attr in k:
    #             print(k[attr])

    # buy(data_comp)
    constAsk()
    constBid()
    supply()
    demand()
    getMatchOrder()
    newMarketP()
    print('seperator ',rank)
    # print(bidList)
    # print(askList)


MPI.Finalize()
