
from mpi4py import MPI
import numpy as np
import random as rd
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import statistics as stats
import datetime as dt


## VARY after Buy batch trading
currP = 100
newLocalP = currP
globalP = []
newGlobalP = currP


## CONSTANTS
numUser = 500
userList = []

## this will be generated after each trade settlement
## and will be stored in userSellerBuyer
sellersBuyers = []
userSellerBuyer = []

## these will keep track of all the placed by the users
userSellerBuyer = [] 
userOrderType = []

userOrders = []

userLimitOrders = []

stopOrder = []
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
        var = rd.randint(1,4)
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
        if orderType[i] == 1 or orderType[i] == 3 or orderType == 4:
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
            var = var + marketPrice
            askBidMarketList.append(var)
        elif orderType[i] == 2: ## order type is market than prices = market price
            askBidMarketList.append(marketPrice)
        else:
            askBidMarketList.append(None)
    return askBidMarketList

def cobineLimitOrders(userLimitOrders, userOrders):
    


def getMatchOrders(userList, sellersBuyers, orderType, userOrders):
    
    listSell = []
    listBuy = []
    ## seperating sellers and buyers
    for i in range(len(userList)):
        if sellersBuyers[i] == 0:
            listSell.append([i, orderType[i], userOrders[i]])
        else:
            listBuy.append([i, orderType[i], userOrders[i]])

    ## 1) pass: matching orders for ask/buy and market orders.

    ## firstly settling the trades of ask and bid
    ## first settling ask bid and market price orders
    ## matchList: [...[sellerID, buyerID, price]...]

    matchList = []
    remainingUnMatchOrdersBuy = []
    remainingUnMatchOrdersSell = []


    listAskBidMarketSell = []
    listLimitStopSell = []

    listAskBidMarketBuy = []
    listLimitStopBuy = []


    for i in range(len(listSell)):
        if listSell[i][1] == 1 or listSell[i][1] == 2: 
            listAskBidMarketSell.append(listSell[i])
        else:
            listLimitStopSell.append(listSell[i])

    for i in range(len(listBuy)):
        if listBuy[i][1] == 1 or listBuy[i][1] == 2:
            listAskBidMarketBuy.append(listBuy[i])
        else:
            listLimitStopBuy.append(listBuy[i])

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
            remainingUnMatchOrdersSell.append(listAskBidMarketSell[i])
            j = j + 1
            k = k + 1
        else:
            # matchList.append([ listAskBidMarketSell[j][0], listAskBidMarketBuy[i][0], listAskBidMarketBuy[i][2] ] )
            i = i + 1
            j = j + 1
            
    ## 2) pass: matching orders for limit orders.

    listLimitOrdersSell = []
    listLimitOrdersBuy = []

    listStopOrdersSell = []
    listStopOrdersBuy = []

    for i in range(len(listLimitStopSell)):
        if listLimitOrdersSell[i][1] == 3: 
            listLimitOrdersSell.append(listLimitStopSell[i])
        else:
            listStopOrdersSell.append(listLimitStopSell[i])

    for i in range(len(listLimitStopBuy)):
        if listLimitOrdersBuy[i][1] == 3: 
            listLimitOrdersBuy.append(listLimitStopBuy[i])
        else:
            listStopOrdersBuy.append(listLimitStopBuy[i])


    listLimitOrdersBuy = sorted(listLimitOrdersBuy, key=lambda x : x[2])
    listLimitOrdersSell = sorted(listLimitOrdersSell, key=lambda x : x[2])
    remainingUnMatchOrdersBuy = sorted(listLimitOrdersSell, key=lambda x : x[2])

    ## Simple limit matching algorithm first sorting and then start matching trades.
    ## All the trades which are unmatched will be matched with the limit orders.

    ## first trying to match (listLimitOrdersSell) with (remainingUnMatchOrdersBuy)

    i = 0
    j = 0

    while i < len(listLimitOrdersSell) and j < len(remainingUnMatchOrdersBuy):
        if listLimitOrdersSell[i][2] <= remainingUnMatchOrdersBuy[j][2]:
            matchList.append([ listLimitOrdersSell[j][0], remainingUnMatchOrdersBuy[i][0], remainingUnMatchOrdersBuy[i][2] ] )
            i = i + 1
            j = j + 1
        else:
            j = j + 1
            remainingUnMatchLimitOrdersSell.append(listLimitOrdersSell[i])

    return matchList



#for i in range(10):

## i is the ith batch of trade settlement
## generation step, Front office

userList = createUserList(numUser)


sellersBuyers = decideSellersBuyers(userList)
userSellerBuyer.append(sellersBuyers)

orderType = decideUserOrderType(userList)
userOrderType.append(orderType)

userOrder = createuseruserOrders("none", userList, orderType, currP)
userOrders.append(userOrder)

## We need to maintain list of limit orders combined with all the limit orders of past so that we can settle them in future.
## Taking Limit orders from past batches and merging with the new limit orders.

matchList = getMatchOrders(userList, sellersBuyers, orderType, userOrders)


print(matchList)

#print(userList,sellersBuyers, userMarketOrder, userLimitOrder, useruserOrders, userStopOrder)
