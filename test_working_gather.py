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
newLocalP = currP
globalP = []
bidList = []
askList = []
matchList = []
askAvg = 0
bidAvg = 0

def constBid():
    bidList = []
    for x in range(20):
        var = rd.randint(-100,100)
        var = var/75
        var = float("{0:.3f}".format(var))
        bidList.append(var)
    bidList.sort()
    return bidList

def constAsk():
    askList = []
    for x in range(20):
        var = rd.randint(-100,100)
        var = var/75
        var = float("{0:.3f}".format(var))
        askList.append(var)
    askList.sort()
    return askList

# ask prices determines the supply of the stock
def supply(askList):
    var = 0
    if askList != None:
        for key in askList:
            var = var + key
    var = float("{0:.3f}".format(var))
    return var

#  similarly bid prices determine the demand of the stock
def demand(bidList):
    var = 0
    if bidList != None:
        for key in bidList:
            var = var + key
    var = float("{0:.3f}".format(var))
    return var


# settling of orders from differnt traders
def getMatchOrder(askList,bidList):
    matchList = []
    if askList != None and bidList != None:
        matchList = list(set(askList).intersection(bidList))
    list2 = []
    if matchList != None:
        for k in matchList:
            list2.append(currP + k)
    list2.sort()
    return list2

# after different settlements new prices are projected on the market
def newLocalMarketP(matchList,currP):
    var = 0
    nlp = currP
    lenMatch = len(matchList)
    if lenMatch != 0:
        for k in matchList:
            var = var + k
        nlp = var/lenMatch
        nlp = float("{0:.3f}".format(nlp))
    return nlp

if rank == 0:
    # print('Entering the 0th processes')
    data_comp = {
                'c1' : {'mp': '12',
                        'ask': '13',
                        'bid': '11'}
                }
    for i in range(1,numProcess):
        comm.send(data_comp,dest=i)

    askList = constAsk()
    bidList = constBid()
    askAvg = supply(askList)
    bidAvg = demand(bidList)
    matchList = getMatchOrder(askList,bidList)
    newLocalP = newLocalMarketP(matchList, currP)
    print('rank, askAvg, bidAvg, last trades, newP ',rank, askAvg, bidAvg, matchList, newLocalP)

else:
    data_comp = comm.recv(source=0)
    askList = constAsk()
    bidList = constBid()
    askAvg = supply(askList)
    bidAvg = demand(bidList)
    matchList = getMatchOrder(askList,bidList)
    newLocalP = newLocalMarketP(matchList, currP)
    print('rank, askAvg, bidAvg, last trades, newP ',rank, askAvg, bidAvg, matchList, newLocalP)

for i in range(0,numProcess-1):
    np = comm.bcast(newLocalP, root=i)
    globalP.append(np)

print(rank,globalP)
MPI.Finalize()
