import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy as sp
import random as rnd
from utils import *
from scipy import vectorize
#from matplotlib2tikz import save as tikz_save      #If export to tikz should be used

from sea import *
from market import *
from plotTool import *

def cap_gen(size, prob, val=1):
    return val * (sp.random.random(size) < prob) + 1e-6*sp.ones(size)

if __name__ == '__main__':
    xsize = 10
    ysize = 10
    num_fishermans = 10
    num_fish_species = 2
    initial_pop = 0.5
    capacity = 1

    allee = 0.1
    #cap_mat = capacity * sp.ones((xsize,ysize))
    #cap_mat += 0.1 * ( sp.random.random(cap_mat.shape) - 0.5 )
    cap_mat = [ cap_gen((xsize,ysize), 0.5, initial_pop), cap_gen((xsize,ysize), 0.3, initial_pop)]
    
    print(cap_mat)
    
    allee_effect = 0.1;
    growth_rate = 1
    threshs = 0
    greeds = 0

    intial_price = (1,2)
    market_demand = (0.1,0.4)

    harvest_fractions = 0.18

    days = 200

    fish_population_log = sp.zeros((num_fish_species,xsize*ysize, days))
    fisherman_wealth_log = sp.zeros((num_fishermans, days))
    price_log = sp.zeros((num_fish_species,days))

    s = Sea((xsize, ysize), num_fishermans, harvest_fractions, threshs, greeds, num_fish_species, growth_rate, initial_pop, cap_mat, allee)
    market = Market(intial_price, market_demand)

    for day in range(days):
        s.day_dynamics()
        market.sell(s.fishermans_list)

        for i,price in enumerate(market.price):
            price_log[i][day] = price
            #print(price_log[i][day])


        for i in range(num_fishermans):
            fisherman_wealth_log[i][day] = s.fishermans_list[i].wealth



        for x in range(xsize):
            for y in range(ysize):
                for specie, fishes in enumerate(s.fishes_list):
                    fish_population_log[specie][x*ysize+y][day] = fishes.population[x][y]


    #Plot the result
    plot_fishpop(fish_population_log)
    plt.figure()
    for i in range(num_fishermans):
        plt.plot(sp.arange(0, days), fisherman_wealth_log[i], label = 'Fisherman ' + str(i+1))
    plt.xlabel('Time')
    plt.ylabel('Total Wealth')
    plt.legend()
    plt.figure()
    for i in range(num_fish_species):
        plt.semilogy(sp.arange(0, days), price_log[i], label = 'Specie ' + str(i+1))
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.ylim(0.1,10)
    plt.legend()

    #tikz_save('modeldynamic2.tikz',        #Exporting the figure to tikz format (latex image)
    #       figureheight = '\\figureheight',
    #       figurewidth = '\\figurewidth')


    plt.show()
