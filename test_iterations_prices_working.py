from mpi4py import MPI
import numpy as np
import random as rd
import time

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
newGlobalP = currP
bidList = []
askList = []
matchList = []
askAvg = 0
bidAvg = 0

## Both functions generate a batch of ask and bid prices to be evaluated
## here each batch can contain atmost K bids and asks Both
## After this, there orders are matched or to say the trades are settled,
## which gives us final prices in the local exchanges and each exchange
## broadcasts the prices, so that all other exchanges get aware of the new prices
## so they update their currP.
def constBid():
    bidList = []
    for x in range(20):
        var = rd.randint(-100,100)
        var = var/5
        var = float("{0:.4f}".format(var))
        bidList.append(var)
    bidList.sort()
    return bidList

def constAsk():
    askList = []
    for x in range(20):
        var = rd.randint(-100,100)
        var = var/5
        var = float("{0:.4f}".format(var))
        askList.append(var)
    askList.sort()
    return askList

# ask prices determines the supply of the stock
def supply(askList):
    var = 0
    if askList != None:
        for key in askList:
            var = var + key
    var = float("{0:.4f}".format(var))
    return var

#  similarly bid prices determine the demand of the stock
def demand(bidList):
    var = 0
    if bidList != None:
        for key in bidList:
            var = var + key
    var = float("{0:.4f}".format(var))
    return var


# settling of orders from differnt traders
def getMatchOrder(askList,bidList,currP):
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
        nlp = float("{0:.4f}".format(nlp))
    return nlp

def brCastPrices(newLocalP):
    for i in range(0,numProcess):
        np = comm.bcast(newLocalP, root=i)
        np = float("{0:.4f}".format(np))
        globalP.append(np)
    return globalP

def avgGlobalMarketP(globalP):
    var = 0
    ngmp = currP
    lengmp = len(globalP)
    if lengmp != 0:
        for k in globalP:
            var = var + k
        ngmp = var/lengmp
        ngmp = float("{0:.4f}".format(ngmp))
    return ngmp

def setNewCurrP(currP,newGlobalP):
    currP = newGlobalP
    currP = float("{0:.4f}".format(currP))
    return currP

def startMarket(currP):
    askList = constAsk()
    bidList = constBid()
    askAvg = supply(askList)
    bidAvg = demand(bidList)
    matchList = getMatchOrder(askList,bidList,currP)
    newLocalP = newLocalMarketP(matchList, currP)
    # print('rank, askAvg, bidAvg, last trades, newP ',rank, askAvg, bidAvg, matchList, newLocalP)
    globalP = brCastPrices(newLocalP)
    newGlobalP = avgGlobalMarketP(globalP)
    currP = setNewCurrP(currP, newGlobalP)
    return currP

if rank == 0:
    # print('Entering the 0th processes')
    data_comp = {
                'c1' : {'mp': '12',
                        'ask': '13',
                        'bid': '11'}
                }
    # for i in range(1,numProcess):
    #     comm.send(data_comp,dest=i)


    for i in range(1000):
        currP = startMarket(currP)
        currP = float("{0:.4f}".format(currP))
        print(i,currP*100)
        time.sleep(0.1)

else:
    for i in range(1000):
        currP = startMarket(currP)
        time.sleep(0.1)

MPI.Finalize()
