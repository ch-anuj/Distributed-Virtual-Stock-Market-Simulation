    # companyList = {
    #   "comp1": "pwdC1",
    #   "comp2": "pwdC2",
    #   "comp3": "pwdC3",
    #   "comp4": "pwdC4"
    #   }
    # bankList = {
    #   "bank1": "pwdB1",
    #   "bank2": "pwdB2",
    #   "bank3": "pwdB3",
    #   "bank4": "pwdB4"
    #   }


from mpi4py import MPI
import numpy as np
import random
# import matplotlib.pyplot as plt
# from matplotlib.finance import candlestick


compStocks = []
banks = 0
logFile = "" #history


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

    def bid(self, stockName, quantity, price):
        pass

    def ask(self, stockName, quantity, price):
        pass

    def updatePortfolio(self,userID):
        pass

    def getPortfolioValue(self,userID):
        pass

    def printPortfolio(self,userID):
        pass

    def getPortfolio(self):
        pass

    def adductionToPortfolio(self,userID):
        pass

    def PlotStock(self, stockName):
        pass


# user list will have different entites which will be trading with different strategies
# our final goal will be to calculate who will be the winner of the game/simulation and
# which strategy is better.

# Each client will start with a fixed amount of money and they
# can make more money or loose money in the game
clientsList = []
clientsPerRank = 3

if rank == 0:
    SE0 = StockExchange("SE0")
    print('Entering the 0th processes')
    # clientsList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    clientsList = np.linspace(1,numProcess*clientsPerRank,clientsPerRank*numProcess)

recvbuf = np.empty(clientsPerRank, dtype='d') # allocate space for lists
comm.Scatter(clientsList, recvbuf, root=0)
nameOfSE = "SE" + str(rank) #like SE0, SE1, SE2..., SEn. where n is number of processes.
IthSE = StockExchange(nameOfSE)
print(clientsList)


MPI.Finalize()
