import mysql.connector as SQL
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
class StockExchange(object): #Trader, Bank, Comp):
    def __init__(self, name):
        self.name = name

    def CreateClientDB():
        mydb = SQL.connect(
            host="localhost",
            user="anujc",
            passwd="anujchauhan"
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE ClientPortfolio")

    def EditClientDB():
        mydb = SQL.connect(
            host="localhost",
            user="anujc",
            passwd="anujchauhan",
            database="ClientPortfolio"
        )

        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE Clients (name VARCHAR(255), id VARCHAR(255), pwd VARCHAR(255), Value VARCHAR(255))")


    def ShowClientDB():
        mydb = SQL.connect(
            host="localhost",
            user="anujc",
            passwd="anujchauhan",
        )

        mycursor = mydb.cursor()
        mycursor.execute("SHOW DATABASES")
        for x in mycursor:
          print(x)

    # user list will have different entites which will be trading with different strategies
    # our final goal will be to calculate who will be the winner of the game/simulation and
    # which strategy is better.

clientsList =	{
  "client1": "password1",
  "client2": "password2",
  "client3": "password3",
  "client4": "password4",
  }
