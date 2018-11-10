from mpi4py import MPI
import numpy as np
import random as rd
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import statistics as stats
import datetime as dt




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
highLow = [ currP, currP] # just record the high and low price at which the stock that is tradded
rumourInGM = ""
localTime = 0
globalLows = []
globalHighs = []
globalLow = currP
globalHigh = currP
## Both functions generate a batch of ask and bid prices to be evaluated
## here each batch can contain atmost K bids and asks Both
## After this, there orders are matched or to say the trades are settled,
## which gives us final prices in the local exchanges and each exchange
## broadcasts the prices, so that all other exchanges get aware of the new prices
## so they update their currP.

## if highest bid is high then this implies that demand is increasing
## if highest bid is falling then this implies the demand is decreasing
## getting highest bid
def incLocalTime(localTime):
    return localTime+1

def constBid(rumour):
    # localTime = incLocalTime(localTime)
    # if localTime >= 200 and localTime <= 300:
    #     rumour = "rise"
    # else:
    #     rumour = "fall"
    bidList = []
    for x in range(100):
        if rumour == "none" :
            var = rd.randint(-100,100)
        elif rumour == "rise":
            var = rd.randint(-90,100)
        elif rumour == "fall":
            var = rd.randint(-100,90)
        else:
            pass
        k = rd.randint(5,10)
        var = var/k
        var = float("{0:.4f}".format(var))
        bidList.append(var)
    bidList.sort()
    return bidList
## if the lowest ask is increasing then this implies value of stock is increasing
## if the lowest ask is decreasing then this implies value of stock is decreaisng

def constAsk(rumour):
    # localTime = incLocalTime(localTime)
    # if localTime >= 200 and localTime <= 300:
    #     rumour = "rise"
    # else:
    #     rumour = "fall"
    askList = []
    for x in range(100):
        if rumour == "none" :
            var = rd.randint(-100,100)
        elif rumour == "rise":
            var = rd.randint(-90,100)
        elif rumour == "fall":
            var = rd.randint(-100,90)
        else:
            pass
        k = rd.randint(5,10)
        var = var/k
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
    list2 = []
    if askList != None and bidList != None:
        list2 = list(set(askList).intersection(bidList))
    matchList = []
    if list2 != None:
        for k in list2:
            matchList.append(currP + k)
    matchList.sort()
    return matchList

def findHighLow(highLow,matchList):
    newHighLow = []
    # highLow.append(matchList[1])
    # highLow.append(matchList[len(matchList)])
    if matchList is None:
        low =  highLow[0]
        high = highLow[1]
    elif  len(matchList) == 1 :
        low = matchList[0]
        high = matchList[1]
    else:
        low = matchList[0]
        high = matchList[-1]

    newHighLow.append(low)
    newHighLow.append(high)
    return newHighLow

## after different settlements new prices are projected on the market
## IDEALY PRICES ARE DETERMINED BY VERY BIG ALGORITHMS WHICH PLOT supply
## AND DEMAND CURVES AND CALCULATE PRICES BY TAKING THE INTERSECTION OF THOSE CURVES.
def newLocalMarketP(matchList,currP):
    var = 0
    nlp = currP
    lenMatch = len(matchList)
    if lenMatch != 0:
        # for k in matchList:
        #     var = var + k
        # nlp = var/lenMatch

        nlp = stats.median(matchList)

        # nlp = stats.mode(matchList)

        # nlp = max(matchList, key = matchList.count)

        # nlp = rd.choice(matchList)

        # k = rd.randint(1,10)
        # list1 = matchList[ 1 :: int(lenMatch/3) ]
        # list2 = matchList[ (int(lenMatch/3)+1) :: ( int(lenMatch*(2/3) )+1 )]
        # list3 = matchList[ ( int(lenMatch*(2/3) )+1 ) :: lenMatch]
        #
        # if k == 1 or k == 2:
        #     if list2 is None:
        #         nlp = rd.choice(matchList)
        #     else:
        #         nlp = rd.choice(list2)
        #
        # elif k == 3 or k == 4 or k == 5 or k == 6:
        #     if list1 is None:
        #         nlp = rd.choice(matchList)
        #     else:
        #         nlp = rd.choice(list1)
        # else:
        #     if list3 is None:
        #         nlp = rd.choice(matchList)
        #     else:
        #         nlp = rd.choice(list3)

        nlp = float("{0:.4f}".format(nlp))
    return nlp

def brCastPrices(newLocalP):
    for i in range(0,numProcess):
        np = comm.bcast(newLocalP, root=i)
        np = float("{0:.4f}".format(np))
        globalP.append(np)
    return globalP

def brCastLow(low):
    globalLow = []
    for i in range(0,numProcess):
        np = comm.bcast(low, root=i)
        np = float("{0:.4f}".format(np))
        globalLow.append(np)
    return globalLow

def brCastHigh(high):
    globalHigh = []
    for i in range(0,numProcess):
        np = comm.bcast(high, root=i)
        np = float("{0:.4f}".format(np))
        globalHigh.append(np)
    return globalHigh

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

## Now for making simulaion more real we can add Rumors to the market like
## there will be a rumour function taking argument like prices will rise of fall
## which i basic form of rumour

def rumourInMaret(rumour):
    if rumour == None:
        return "none"
    elif rumour == "Companies are performing good":
        return "rise"
    elif rumour == "Companies are performing bad":
        return "fall"
    else:
        return "none"


def startMarket(highLow, currP):
    rumourInGM = rumourInMaret("weather is cold outside")
    askList = constAsk(rumourInGM)
    bidList = constBid(rumourInGM)
    askAvg = supply(askList)
    bidAvg = demand(bidList)
    matchList = getMatchOrder(askList,bidList,currP)

    newLocalP = newLocalMarketP(matchList, currP)
    # print("rank, newLocalP", rank, newLocalP)
    globalP = brCastPrices(newLocalP)
    newGlobalP = avgGlobalMarketP(globalP)
    currP = setNewCurrP(currP, newGlobalP)

    highLow = findHighLow(highLow, matchList)
    # print("local highLow",rank, highLow)
    localLow = highLow[0]
    localHigh = highLow[-1]
    globalLows = brCastLow(localLow)
    globalHighs = brCastHigh(localHigh)
    globalLows.sort()
    globalHighs.sort()
    highLow.clear()
    highLow.append(globalLows[0])
    highLow.append(globalHighs[-1])

    # print('rank, last trades, newP, globalLow, globalHigh',rank, highLow)

    return currP

def plot_init():
    ax1 = plt.subplot2grid((1,1), (0,0))
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title("Projected stock prices of XYZ")
    plt.xlabel('Time')
    plt.ylabel('Prices')
    ax1.grid(True)

    # plt.axis([-1, 11, -1.5, 1.5]);
    # plt.legend()

K_for_time = 1000

if rank == 0:

    # print('Entering the 0th processes')
    plot_init()
    for i in range(K_for_time):
        currP = startMarket(highLow,currP)
        currP = float("{0:.4f}".format(currP))

        # plt.scatter(i,currP, color='k', s=10)
        ncp = currP*100
        plt.scatter(i, ncp, color='black', s = 1)
        ## Fast Version
        plt.pause(0.0001)

        ## Slow Version
        # plt.pause(1.0)
        print(i,ncp)

        # time.sleep(0.1)
    plt.show()

else:
    # print('Entering the rank_th processes')

    for i in range(K_for_time):
        currP = startMarket(highLow,currP)
        time.sleep(0.1)

MPI.Finalize()
