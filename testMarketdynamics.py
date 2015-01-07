import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy as sp
import random as rnd
from utils import *
#import sciy.vectorize

tikzsave = False
if tikzsave:
    from matplotlib2tikz import save as tikz_save      #If export to tikz should be used

from sea import *
from marketAlt import *
from plotTool import *

if __name__ == '__main__':
    print('Setting 1: one common, one rare specie, small grid')
    print('Setting 2: one common, one crisscross, large grid')
    print('Setting 3: one common, rare one crisscross, large grid')
    print('Setting 4: multiple differnet species, large grid')

    setting = int(input("Enter setting (1-4): "))

    if setting ==1:
        xsize = 2
        ysize = 2
        capacity = 1
        num_fishermans = 2
        num_fish_species = 2
        cap_mat = capacity * sp.ones((num_fish_species,xsize,ysize))
        cap_mat[1] = sp.array([[1e-6, 1e-6],[1,1e-6]])
        harvest_fractions = 0.1
        days = 500
    elif setting==2:
        xsize = 6
        ysize = 6
        capacity = 1
        num_fishermans = 15
        num_fish_species = 2
        cap_mat = capacity * sp.ones((num_fish_species,xsize,ysize))
        cap_mat[1] = crisscross_mat(capacity,(xsize,ysize))
        print(cap_mat)
        harvest_fractions = 0.1
        days = 1000
    elif setting==3:
        xsize = 6
        ysize = 6
        capacity = 1
        num_fishermans = 12
        num_fish_species = 2
        cap_mat = capacity * sp.ones((num_fish_species,xsize,ysize))
        cap_mat[1] = crisscross_mat(capacity,(xsize,ysize),1e-6)
        harvest_fractions = 0.20
        days = 1000
    elif setting==4:
        xsize = 6
        ysize = 6
        capacity = 1
        num_fishermans = 8
        num_fish_species = 4
        cap_mat = capacity * sp.ones((num_fish_species,xsize,ysize))
        cap_mat[1] = crisscross_mat(capacity,(xsize,ysize),1e-6)
        cap_mat[2] = sp.rand(xsize,ysize)
        cap_mat[3] = crisscross_mat(capacity,(xsize,ysize))
        harvest_fractions = 0.20
        days = 500
    else:
        print('Invalid input, Termiates')
        exit()
    initial_pop = 0.8

    allee = 0.1

    #cap_mat += 0.1 * ( sp.random.random(cap_mat.shape) - 0.5 )
    allee_effect = 0.1;
    growth_rate = 0.1
    fisher_behavior = 1

    #intial_price = (0.1,0.2,0.1)
    #market_demand = (0.12,0.4,0.12) not used with the other market dynamics


    fish_population_log = sp.zeros((num_fish_species,xsize*ysize, days))
    fisherman_wealth_log = sp.zeros((num_fishermans, days))
    price_log = sp.zeros((num_fish_species,days))
    fishing_regime_log=sp.zeros((num_fish_species,days))
    level = sp.zeros(num_fishermans)

    s = Sea((xsize, ysize), num_fishermans, harvest_fractions, 0, 0, num_fish_species, growth_rate, initial_pop, cap_mat, allee, fisher_behavior, level)

    market = Market(sp.mean(sp.mean(cap_mat,2),1)*initial_pop)

    for day in range(days):
        s.day_dynamics()
        fishermen_targets=sp.zeros(num_fish_species)
        for sailor in s.fishermans_list:
            #print(sailor.catch)
            fishermen_targets[sailor.catch[0]]+=1/num_fishermans
        #print(fishermen_targets)
        fishing_regime_log[:,day]=fishermen_targets
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
    print(fishing_regime_log)
    t = sp.arange(0, days)
    if (tikzsave):
        plot_fishpop(fish_population_log)
        tikz_save('fishpopmarket.tikz',        #Exporting the figure to tikz format (latex image) Doesn't work for some reason
            figureheight = '\\figureheight',
            figurewidth = '\\figurewidth')

    else:
        plt.figure()
        n_species = fish_population_log.shape[0]
        colvec = [plt.cm.winter(i) for i in sp.linspace(0, 0.9, n_species)]
        n_pops = fish_population_log.shape[1]
        days = fish_population_log.shape[2]
        for i in range(n_species):
            masked_pops = sp.ma.masked_equal(fish_population_log[i], 0)
            avg_fishpop = sp.mean(masked_pops, axis=0)
            plt.plot(t,avg_fishpop, label = 'Specie '+ str(i+1))
        plt.xlabel('Time')
        plt.ylabel('Fish population')
        plt.legend()



    if False:
        plt.figure()
        for i in range(num_fishermans):
            plt.plot(t, fisherman_wealth_log[i], label = 'Fisherman ' + str(i+1))
        plt.xlabel('Time')
        plt.ylabel('Total Wealth')
        plt.legend()

    plt.figure()
    for i in range(num_fish_species):
        plt.semilogy(t, price_log[i], label = 'Specie ' + str(i+1))
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    if tikzsave:
        tikz_save('pricemarket.tikz',        #Exporting the figure to tikz format (latex image)
            figureheight = '\\figureheight',
            figurewidth = '\\figurewidth')


    plt.figure()
    for i in range(num_fish_species):
        plt.plot(range(days),fishing_regime_log[i])
    plt.show()
