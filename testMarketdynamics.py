import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy as sp
import random as rnd
from utils import *
#import sciy.vectorize
#from matplotlib2tikz import save as tikz_save      #If export to tikz should be used

from sea import *
from marketAlt import *
from plotTool import *

if __name__ == '__main__':
    xsize = 2
    ysize = 2
    num_fishermans = 4
    num_fish_species = 2
    initial_pop = 0.5
    capacity = 1
    allee = 0.1
    cap_mat = capacity * sp.ones((num_fish_species,xsize,ysize))
    cap_mat[1] = sp.array([[0.5, 1e-6],[0.5,1e-6]])
    #cap_mat += 0.1 * ( sp.random.random(cap_mat.shape) - 0.5 )
    allee_effect = 0.1;
    growth_rate = 0.5
    move_each_day = False

    #intial_price = (0.1,0.2,0.1)
    #market_demand = (0.12,0.4,0.12) not used with the other market dynamics

    harvest_fractions = 0.3

    days = 2000

    fish_population_log = sp.zeros((num_fish_species,xsize*ysize, days))
    fisherman_wealth_log = sp.zeros((num_fishermans, days))
    price_log = sp.zeros((num_fish_species,days))

    s = Sea((xsize, ysize), num_fishermans, harvest_fractions, 0, 0, num_fish_species, growth_rate, initial_pop, cap_mat, allee, move_each_day)


    market = Market(sp.mean(sp.mean(cap_mat,2),1)*initial_pop)

    for day in range(days):
        s.day_dynamics()
        market.sell(s.fishermans_list)

        for i,price in enumerate(market.price):
            price_log[i][day] = price


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
    plt.legend()

    #tikz_save('modeldynamic2.tikz',        #Exporting the figure to tikz format (latex image)
    #       figureheight = '\\figureheight',
    #       figurewidth = '\\figurewidth')


    plt.show()
