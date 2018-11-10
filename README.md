TO RUN THE VIRTUAL STOCK MARKET SIMULATION
============================================
``` mpirun --oversubscribe -n <number_of_stockexchange> python <file_name>```

# THERE ARE 3 PHASES:

# FRONT OFFICE : Traders and orders will be created.

- there are N users in each SE having 2 options to buy or sell their stock.
- they have 4 options/(types of orders) to sell(0) or buy(1):
        
        1:: traded at Ask/Bid prices
        2:: traded at market prices
        3:: traded at Limit prices (>= || <=: prices)
        4:: traded at market price if hit the userStopOrder
        
- all the options will be generated randomly to simulate a market with many users
different tunning are done to make graphs look like real markets.

#### Functions in the first section are
 
1) createUserList(K):
- will return the list of users from 0 to k-1

2) decideSellersBuyers(userList):
- will return a list of 0s and 1s sucht that if genBits[i] = 0 then i is selling stock and if genBits[i] = 1 then i is buying stock.

3) decideUserOrderType(userList):
- will return a list having each entry between 1 and 4, so if list[i] = 1 then order type = ask/bid, and similar for other orders.

4) createUserOrders(rumour, userList, orderType, marketPrice):        
- will return a list of prices of orders based on the random generation having a window of prices fixed s.t. the maximmum fluctuation must be in that window.

5) supply(askList):
- this is to furthur extend the project for calculating supply of stocks in the market.

6) demand(bidList):
- this is to furthur extend the project for calculating demand of stocks in the market.

# MIDDLE OFFICE: Trades will be matched.

#### Functions in the first section are

1) getMatchOrders(userList, sellersBuyers, orderType, userOrders, marketPrice, userStopOrdersSell, userStopOrdersBuy):
- there are 4 passes in this Functions.
- first pass is for stop orders.
- second pass is for ask/bid and market orders.
- third pass is for limit orders.
- fourth pass is for remaining limit orders among each other.

# BACK OFFICE: Prices will be broadcasted and updated.

#### Functions in the first section are

1) findHighLow(highLow,matchList):
- this will return the local high and low of the stock.

2) newLocalMarketP(listM,currP):
- this will return the new local market price using different approches.

3) avgGlobalMarketP(globalP):
- this will return the new global market price using different approaches.

4) setNewCurrP(currP,newGlobalP):
- for setting the currP = newGlobalP.

5) brCastPrices(newLocalP):
- for broadcasting the local prices so that all exchanges would update their globalP list.

6) brCastLow(low):
- for broadcasting the local lows.

7) brCastHigh(high):
- for broadcasting the local highs.

8) plot_init():
- for initialising the plots.

9) startMarket(highLow,currP):
- this function contains all the different functions in specific order to sequentially execute the program.

# PLATFORM : mpi4py in python is used for communication between the processes


# REFERENCES

1) https://www.investopedia.com/exam-guide/series-65/trading-securities/order-types.asp

2) https://rabernat.github.io/research_computing/parallel-programming-with-mpi-for-python.html

3) https://pythonprogramming.net/live-graphs-matplotlib-tutorial/

4) https://stackoverflow.com/
