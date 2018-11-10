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
highLow = []
highLow.append(currP)
highLow.append(currP)

## these will remain constant
numUser = 5000
userList = []

## this will be generated after each trade settlement
## and will be stored in userSellerBuyer
sellersBuyers = []
userSellerBuyer = []

## these will keep track of all the placed by the users
userSellerBuyer = [] 
userOrderType = []

userOrders = []

## a list for maintaing all the stop loss orders such that if the stop loss price hits the market price then the order will be placed in the trade queue.

userStopOrdersSell = []
userStopOrdersBuy = []

## a list for mainting settled matched orders.
matchList = []


def createUserList(K):# k = number of clients
    userList = []
    for i in range(K):
        userList.append(i)
    return userList

## there are 3 options
## -1: sell order
## 0: do nothing
## 1: buy order

def decideSellersBuyers(userList):
    genBinList = []
    for i in range(len(userList)):
        var = rd.randint(0,1)
        genBinList.append(var)
    return genBinList
    
## there are 4 types of order
## 1: useruserOrders: traded at Ask/Bid prices
## 2: userMarketOrder: traded at market prices
## 3: userLimitOrder: traded at Limit prices (>= || <=: prices)
## 4: userStopOrder: traded at market price if hit the userStopOrder

def decideUserOrderType(userList):
    genOrderType = []
    for i in range(len(userList)):
        var = rd.randint(1,20)
        if var == 1:
            var = 4
        elif var >= 2 and var <= 4:
            var = 3
        elif var >=5 and var <= 10:
            var = 2
        else:
            var = 1
        genOrderType.append(var)
    return genOrderType



def createuseruserOrders(rumour, userList, orderType, marketPrice):        
    # localTime = incLocalTime(localTime)
    # if localTime >= 200 and localTime <= 300:
    #     rumour = "rise"
    # else:
    #     rumour = "fall"
    askBidMarketList = []
    noOfUsers = len(userList)
    
    for i in range(noOfUsers):
        if orderType[i] == 1 or orderType[i] == 3 or orderType[i] == 4:
            if rumour == "none" :
                var = rd.randint(-50,100)
            elif rumour == "rise":
                var = rd.randint(-20,100)
            elif rumour == "fall":
                var = rd.randint(-100,20)
            else:
                pass
            k = rd.randint(70,150)
            var = var/k
            var = float("{0:.4f}".format(var))
            var = var + marketPrice
            askBidMarketList.append(var)
        else: #orderType[i] == 2: ## order type is market than prices = market price
            askBidMarketList.append(marketPrice)
    return askBidMarketList


## ask prices determines the supply of the stock
def supply(askList):
    var = 0
    if askList != None:
        for key in askList:
            var = var + key
    var = float("{0:.4f}".format(var))
    return var

##  similarly bid prices determine the demand of the stock
def demand(bidList):
    var = 0
    if bidList != None:
        for key in bidList:
            var = var + key
    var = float("{0:.4f}".format(var))
    return var


def getMatchOrders(userList, sellersBuyers, orderType, userOrders, marketPrice, userStopOrdersSell, userStopOrdersBuy):
    listSell = []
    listBuy = []
    ## seperating sellers and buyers
    userOrder = userOrders[-1]
    
    matchList = []
    remainingUnMatchOrdersBuy = []
    remainingUnMatchOrdersSell = []
    
    listAskBidMarketSell = []
    listLimitStopSell = []
    
    listAskBidMarketBuy = []
    listLimitStopBuy = []
    
    listLimitOrdersSell = []
    remainingUnMatchLimitOrdersSell = []
    listLimitOrdersBuy = []
    remainingUnMatchLimitOrdersBuy = []

    listStopOrdersSell = []
    listStopOrdersBuy = []
    
    ## seperating sellers and buyers
    i = 0
    for i in range(len(sellersBuyers)):
        if sellersBuyers[i] == 0:
            listSell.append([ i, orderType[i], userOrder[i] ])
        else:
            listBuy.append([ i, orderType[i], userOrder[i] ])
    i = 0  
    for i in range(len(listSell)):
        if listSell[i][1] == 1 or listSell[i][1] == 2: 
            listAskBidMarketSell.append(listSell[i])
        else:
            listLimitStopSell.append(listSell[i])
    i = 0    
    for i in range(len(listBuy)):
        if listBuy[i][1] == 1 or listBuy[i][1] == 2:
            listAskBidMarketBuy.append(listBuy[i])
        else:
            listLimitStopBuy.append(listBuy[i])
    
    ## now seperating limit and stop orders.
    i = 0
    for i in range(len(listLimitStopSell)):
        if listLimitStopSell[i][1] == 3:
            listLimitOrdersSell.append(listLimitStopSell[i])
        else:
            listStopOrdersSell.append(listLimitStopSell[i])
    i = 0    
    for i in range(len(listLimitStopBuy)):
        if listLimitStopBuy[i][1] == 3: 
            listLimitOrdersBuy.append(listLimitStopBuy[i])
        else:
            listStopOrdersBuy.append(listLimitStopBuy[i])
            
    ## 1) Pass: Matching Stop orders
    ## Appending new stop orders into the previous stop orders 
    
    i = 0
    for i in range(len(listStopOrdersBuy)):
        userStopOrdersBuy.append(listStopOrdersBuy[i])
    
    i = 0
    for i in range(len(listStopOrdersSell)):
        userStopOrdersSell.append(listStopOrdersSell[i])
    
    ## and check for the market price if any one of all the orders hits the market price then place them in the simple ask/bid/market matching lists.
    listStopHittedMarketBuy = []
    listStopHittedMarketSell = []
    i = 0
    for i in range(len(userStopOrdersBuy)):
        if userStopOrdersBuy[i][2] >= marketPrice:
            #userStopOrdersBuy[i][2] = marketPrice
            listStopHittedMarketBuy.append(userStopOrdersBuy[i])
    i = 0
    for i in range(len(userStopOrdersSell)):
        if userStopOrdersSell[i][2] <= marketPrice:
            #userStopOrdersSell[i][2] = marketPrice
            listStopHittedMarketSell.append(userStopOrdersSell[i])
    
    i = 0
    for i in range(len(listStopHittedMarketBuy)):
        listAskBidMarketBuy.append(listStopHittedMarketBuy[i])
    
    i = 0
    for i in range(len(listStopHittedMarketSell)):
        listAskBidMarketSell.append(listStopHittedMarketSell[i])
    
    ## 2) pass: matching orders for ask/buy and market orders.

    ## firstly settling the trades of ask and bid
    ## first settling ask bid and market price orders
    ## matchList: [...[sellerID, buyerID, price]...]

    listAskBidMarketBuy = sorted(listAskBidMarketBuy, key=lambda x : x[2])
    listAskBidMarketSell = sorted(listAskBidMarketSell, key=lambda x : x[2])
    
    i = 0
    j = 0
    k = 0
    ## Simple ask bid matching algorithm
    while i < len(listAskBidMarketBuy) and j < len(listAskBidMarketSell):
        if listAskBidMarketBuy[i][2] < listAskBidMarketSell[j][2]:
            remainingUnMatchOrdersBuy.append(listAskBidMarketBuy[i])
            i = i + 1
            k = k + 1
        elif listAskBidMarketBuy[i][2] > listAskBidMarketSell[j][2]:
            remainingUnMatchOrdersSell.append(listAskBidMarketSell[j])
            j = j + 1
            k = k + 1
        else:
            matchList.append([ listAskBidMarketSell[j][0], listAskBidMarketBuy[i][0], listAskBidMarketBuy[i][2] ] )
            i = i + 1
            j = j + 1
            
            
    ## 3) Pass: Matching limit orders
    ## Simple limit matching algorithm first sorting and then start matching trades.
    ## All the trades which are unmatched will be matched with the limit orders.

    listLimitOrdersBuy = sorted(listLimitOrdersBuy, key=lambda x : x[2])
    listLimitOrdersSell = sorted(listLimitOrdersSell, key=lambda x : x[2])
    remainingUnMatchOrdersBuy = sorted(remainingUnMatchOrdersBuy, key=lambda x : x[2])
    remainingUnMatchOrdersSell = sorted(remainingUnMatchOrdersSell, key=lambda x : x[2])
    
    ## first trying to match (listLimitOrdersSell) with (remainingUnMatchOrdersBuy)
    i = 0
    j = 0
    while i < len(listLimitOrdersSell) and j < len(remainingUnMatchOrdersBuy):
        if listLimitOrdersSell[i][2] <= remainingUnMatchOrdersBuy[j][2]:
            matchList.append([ listLimitOrdersSell[i][0], remainingUnMatchOrdersBuy[j][0], remainingUnMatchOrdersBuy[j][2] ] )
            i = i + 1
            j = j + 1
        else:
            j = j + 1
            remainingUnMatchLimitOrdersSell.append(listLimitOrdersSell[i])
            
    ## and then trying to match (listLimitOrdersBuy) with (remainingUnMatchOrdersSell)
    i = 0
    j = 0
    while i < len(listLimitOrdersBuy) and j < len(remainingUnMatchOrdersSell):
        if listLimitOrdersBuy[i][2] >= remainingUnMatchOrdersSell[j][2]:
            matchList.append([ remainingUnMatchOrdersSell[j][0], listLimitOrdersBuy[i][0], remainingUnMatchOrdersSell[j][2] ] )
            i = i + 1
            j = j + 1
        else:
            remainingUnMatchLimitOrdersBuy.append(listLimitOrdersBuy[i])
            i = i + 1


    ## 4) Pass: Matching remaining limit orders buy and sell against each other
    ## Simple limit matching algorithm first sorting and then start matching trades.
    ## All the trades which are unmatched will be matched with the limit orders.

    i = 0
    j = 0
    while i < len(remainingUnMatchLimitOrdersSell) and j < len(remainingUnMatchLimitOrdersBuy):
        if remainingUnMatchLimitOrdersSell[i][2] <= remainingUnMatchLimitOrdersBuy[j][2]:
            matchList.append([ remainingUnMatchLimitOrdersSell[j][0], remainingUnMatchLimitOrdersBuy[i][0], (remainingUnMatchLimitOrdersSell[j][2] + remainingUnMatchLimitOrdersSell[i][2])/2 ] )
            i = i + 1
            j = j + 1
        else:
            j = j + 1


    #return [listLimitOrdersSell,"############################", remainingUnMatchOrdersBuy, "###################################", matchList]
    
    #return [listLimitOrdersBuy,"############################", remainingUnMatchOrdersSell, "###################################", matchList]
    
    #return [listStopOrdersBuy,"############################", listStopHittedMarketBuy, "###################################", marketPrice]
    
    #return [listAskBidMarketBuy,"############################", listAskBidMarketSell, "###################################", matchList]
    matchList2 = []
    i = 0
    for i in range(len(matchList)):
        matchList2.append(matchList[i][2])
    matchList2.sort()
    return matchList2

## This is to find the local high and low prices at which the trades took place.
def findHighLow(highLow,matchList):
    newHighLow = []
    # highLow.append(matchList[1])
    # highLow.append(matchList[len(matchList)])
    matchList.sort()
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

def newLocalMarketP(listM,currP):
    var = 0
    nlp = currP
    lenMatch = len(listM)
    if lenMatch != 0:
        for k in listM:
            var = var + k
        nlp = var/lenMatch

        #nlp = stats.median(listM)

        #nlp = stats.mode(listM)

        # nlp = max(matchList, key = matchList.count)

        # nlp = rd.choice(listM)

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

def avgGlobalMarketP(globalP):
    var = 0
    ngmp = currP
    lengmp = len(globalP)
    if lengmp != 0:
        #ngmp = stats.median(listM)

        #ngmp = stats.mode(listM)

        # ngmp = max(matchList, key = matchList.count)

        # ngmp = rd.choice(listM)

        # k = rd.randint(1,10)
        # list1 = matchList[ 1 :: int(lenMatch/3) ]
        # list2 = matchList[ (int(lenMatch/3)+1) :: ( int(lenMatch*(2/3) )+1 )]
        # list3 = matchList[ ( int(lenMatch*(2/3) )+1 ) :: lenMatch]
        #
        # if k == 1 or k == 2:
        #     if list2 is None:
        #         ngmp = rd.choice(matchList)
        #     else:
        #         ngmp = rd.choice(list2)
        #
        # elif k == 3 or k == 4 or k == 5 or k == 6:
        #     if list1 is None:
        #         ngmp = rd.choice(matchList)
        #     else:
        #         ngmp = rd.choice(list1)
        # else:
        #     if list3 is None:
        #         ngmp = rd.choice(matchList)
        #     else:
        #         ngmp = rd.choice(list3)

        for k in globalP:
            var = var + k
        ngmp = var/lengmp
        ngmp = float("{0:.4f}".format(ngmp))
    return ngmp

def setNewCurrP(currP,newGlobalP):
    currP = newGlobalP
    currP = float("{0:.4f}".format(currP))
    return currP

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



def plot_init():
    ax1 = plt.subplot2grid((1,1), (0,0))
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title("Projected stock prices of XYZ")
    plt.xlabel('Time')
    plt.ylabel('Prices')
    ax1.grid(True)


def startMarket(highLow,currP):
    
    userList = createUserList(numUser)

    sellersBuyers = decideSellersBuyers(userList)
    userSellerBuyer.append(sellersBuyers)

    orderType = decideUserOrderType(userList)
    userOrderType.append(orderType)

    userOrder = createuseruserOrders("none", userList, orderType, currP)
    userOrders.append(userOrder)

    matchList = getMatchOrders(userList, sellersBuyers, orderType, userOrders, currP, userStopOrdersSell, userStopOrdersBuy)

    newLocalP = newLocalMarketP(matchList, currP)
    # print("rank, newLocalP", rank, newLocalP)
    
    globalP = brCastPrices(newLocalP)
    newGlobalP = avgGlobalMarketP(globalP)
    currP = setNewCurrP(currP, newGlobalP)

    highLow = findHighLow(highLow, matchList)
    # print("local highLow",rank, highLow)
    
    #print(i,"high:", matchList[-1][2], "low: ", matchList[0][2])
    return currP

K_for_time = 1000

if rank == 0: ## Entering 0th process
    plot_init()
    for i in range(K_for_time):
        currP = startMarket(highLow, currP)
        currP = float("{0:.4f}".format(currP))
        
        ncp = currP*100
        ncp = float("{0:.4f}".format(ncp))
        plt.scatter(i, ncp, color='black', s = 2)

        print(i,ncp)
        plt.pause(0.001)
        #time.sleep(0.1)

    plt.show()
else:
    # print('Entering the rank_th processes')
    for i in range(K_for_time):
        currP = startMarket(currP)
        time.sleep(0.1)

MPI.Finalize()
