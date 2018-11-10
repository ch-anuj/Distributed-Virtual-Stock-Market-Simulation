from mpi4py import MPI
import numpy as np
import random
# import matplotlib.pyplot as plt
# from matplotlib.finance import candlestick


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
numProcess = comm.Get_size()


class Trader(object):
    def __init__(self, ID, userPWD, PFolio):
        self.ID = ID
        self.userPWD = userPWD
        self.PFolio = PFolio


class Bank(Trader):
    def __init__(self, ID, userPWD, PFolio):
        ID.__init__(self, ID)
        userPWD.__init__(self, userPWD)
        PFolio.__init__(self, PFolio)


class Comp(Trader):
    def __init__(self, ID, userPWD, PFolio):
        ID.__init__(self, ID)
        userPWD.__init__(self, userPWD)
        PFolio.__init__(self, PFolio)


# Number of stock exchanges will be the number of processes

class StockExchange(object):
    def __init__(self, name):
        self.name = name

    def currentPrices(self):
        return random.randint(1,10)

    def getMarket(self): #output of this method will be the list of companies listed in SE.
        pass

    def getStock(self, stockName):
        pass

    def buyStock(self, stockName, ):
    def updatePortfolio(self,userID):
        pass

    def getPortfolioValue(self,userID):
        pass

    def printPortfolio(self,userID):
        pass

    def getPortfolio(self):
        pass

    def adductionToPortfolio(self,userID)
    # user list will have different entites which will be trading with different strategies
    # our final goal will be to calculate who will be the winner of the game/simulation and
    # which strategy is better.

clientsList =	{
  "client1": "password1",
  "client2": "password2",
  "client3": "password3",
  "client4": "password4"
  }
companyList = {
  "comp1": "passwordC1",
  "comp2": "passwordC2",
  "comp3": "passwordC3",
  "comp4": "passwordC4"
  }

if rank == 0:
    SE0 = StockExchange("SE0")
    print('Entering the 0th processes')
    currentP = SE0.currentPrices()
    print(currentP,"is the current prices in SE0")
    for j in range(numProcess):
        comm.send(currentP, dest = j)

else:
    currentPNew = comm.recv(source=0)
    nameOfSE = "SE" + str(rank) #like SE0, SE1, SE2..., SEn. where n is number of processes.
    IthSE = StockExchange(nameOfSE)
    currentP = IthSE.currentPrices()
    print("Prices after the communication in", nameOfSE, currentPNew, currentP)


MPI.Finalize()
