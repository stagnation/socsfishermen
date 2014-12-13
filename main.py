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
    num_fishermans = 3
    num_fish_species = 2
    initial_pop = 0.5
    capacity = 1
    cap_mat = capacity * sp.ones((xsize,ysize))
    #cap_mat += 0.1 * ( sp.random.random(cap_mat.shape) - 0.5 )
    cap_mat = [ cap_gen((xsize,ysize), 0.8, initial_pop), cap_gen((xsize,ysize), 0.3, initial_pop)]

    cap_mat = std_cap()



    growth_rate = 0.1
    threshs = 0
    greeds = 0
    allee = sp.inf

    intial_price = (1,2)
    market_demand = (0.1,0.4)

    harvest_fractions = 0.5

    days = 1000
    evaluations = 5

    fish_plot = True
    wealth_plot = False
    price_plot = False
    extinct_plot = True
    fish_population_log = 0
    fisherman_wealth_log = 0
    price_log = 0
    entinction_log = 0
    move_each_day = True
    extinction_log = [[],[]]
    for eval in range(evaluations):
        print("eval number", eval)
        fish_population_log = sp.zeros((num_fish_species,xsize*ysize, days))
        fisherman_wealth_log = sp.zeros((num_fishermans, days))
        price_log = sp.zeros((num_fish_species,days))

        s = Sea((xsize, ysize), num_fishermans, harvest_fractions, threshs, greeds,
     num_fish_species, growth_rate, initial_pop, cap_mat, allee, move_each_day)
        market = Market(intial_price, market_demand)

        for day in range(days):
            if day % 500 == 0:
                print("day",day)
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


            if extinct_plot:
                for f in range(num_fish_species):
                    for pop in range( xsize * ysize ):
                        if fish_population_log[f][pop][0] > 0: #day 1 or zero here?
                            extinction_time = is_extinct(fish_population_log[f][pop])
                            extinction_log[f].append(extinction_time)
    #
    #
    #end of evaluations loop
    #
    #
    extinct = sp.zeros(len(extinction_log))
    ext_std = sp.zeros_like(extinct)
    for i,log in enumerate(extinction_log):
        extinct[i] = sp.mean(log)
        ext_std[i] = sp.std(log)
    print(extinction_log)
    print(extinct)
    print(ext_std)


    #Plot the result


    if fish_plot:
        plot_fishpop(fish_population_log)
    if wealth_plot:
        for i in range(num_fishermans):
            plt.plot(sp.arange(0, days), fisherman_wealth_log[i], label = 'Fisherman ' + str(i+1))
        plt.xlabel('Time')
        plt.ylabel('Total Wealth')
        plt.legend()
        plt.figure()
    if price_plot:
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
