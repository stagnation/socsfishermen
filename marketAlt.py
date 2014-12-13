#-------------------------------------------------------------------------------
# Name:        marketClass
# Author:      Edvin
#
# Created:     06-12-2014
#-------------------------------------------------------------------------------
import scipy as sp
class Market:
    max_price = 1e2
    def __init__(self, initial_price):
        self.price = initial_price
        self.num_goods = len(initial_price)

    def sell(self, fisherman_list):
        total_trade = sp.zeros(self.num_goods)
        for fisherman in fisherman_list:
            (goods, amount) = fisherman.catch
            total_trade[goods] += amount
            fisherman.wealth += amount * self.price[goods]
            fisherman.price_perception = self.price
            fisherman.catch = (0,0)

        self.price_responce(total_trade)
    def set_price_zero(self,goods):
        self.price[goods] = 0

    def price_responce(self, total_trade): #P = 1/(Q+eps)^pow
        eps = 1e-3
        my = 0.05
        pow = 2
        previous_trade = sp.divide(1,sp.power(self.price,1/pow)) - eps
        new_trade = previous_trade * (1 - my) + my * total_trade
        self.price = sp.divide(1,sp.power(new_trade+eps,pow))


        #base = 1.1;                         #This could be implemented a parameter as well, it defines the switness in market change. values 1->infty
        #self.price = sp.multiply(self.price, sp.power(base, self.market_demand - total_trade))
        #self.price = sp.minimum(self.price, Marketv2.max_price)

    def  __str__(self):
        return(str(self.x))