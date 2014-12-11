#-------------------------------------------------------------------------------
# Name:        marketClass
# Author:      Edvin
#
# Created:     06-12-2014
#-------------------------------------------------------------------------------
import scipy as sp
class Market:
    max_price = 1e2
    def __init__(self, initial_price,market_demand):
        self.price = initial_price
        self.market_demand = market_demand
        self.num_goods = len(market_demand)

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

    def price_responce(self, total_trade):
        base = 1.1;                         #This could be implemented a parameter as well, it defines the switness in market change. values 1->infty
        self.price = sp.multiply(self.price, sp.power(base, self.market_demand - total_trade))
        self.price = sp.minimum(self.price, Market.max_price)

    def  __str__(self):
        return(str(self.x))