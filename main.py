import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as sp
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
    #cap_mat = [ cap_gen((xsize,ysize), 0.8, initial_pop), cap_gen((xsize,ysize), 0.3, initial_pop)]

    cap_mat = std_cap()



    growth_rate = 0.1
    threshs = 0
    greeds = 0
    allee = sp.inf

    intial_price = (1,2)
    market_demand = (0.1,0.4)

    harvest_fractions = 0.45

    days = 23000
    evaluations = 10

    fish_plot = False
    wealth_plot = False
    price_plot = False
    extinct_plot = True
    fish_population_log = 0
    fisherman_wealth_log = 0
    price_log = 0
    entinction_log = 0
    extinction_log = [[],[]]
    #behavior = 1 #1 for move each day, 2 for move each day but no return
    
    def evaluate( behavior ):
        print("behaviorbehaviorbehaviorbehaviorbehavior", behavior)
        extinction_log = sp.zeros((num_fish_species, evaluations, xsize*ysize))
        for e in range(evaluations):
            print(behav, "eval number", e)
            fish_population_log = sp.zeros((num_fish_species,xsize*ysize, days))
            fisherman_wealth_log = sp.zeros((num_fishermans, days))
            price_log = sp.zeros((num_fish_species,days))

            s = Sea((xsize, ysize), num_fishermans, harvest_fractions, threshs, greeds,
         num_fish_species, growth_rate, initial_pop, cap_mat, allee, behavior)
            market = Market(intial_price, market_demand)

            for day in range(days):
                if day % 500 == 0:
                    print("day",day)
                survive = s.day_dynamics()
                if not survive:
                    print("all extinct day", day)
                    break
                
                market.sell(s.fishermans_list)
    
                for i,price in enumerate(market.price):
                    price_log[i][day] = price

                for i in range(num_fishermans):
                    fisherman_wealth_log[i][day] = s.fishermans_list[i].wealth

                for x in range(xsize):
                    for y in range(ysize):
                        for specie, fishes in enumerate(s.fishes_list):
                            fish_population_log[specie][x*ysize+y][day] = fishes.population[x][y]

            #end of day loop
            if extinct_plot:
                for f in range(num_fish_species):
                    for pop in range( xsize * ysize ):
                        #if fish_population_log[f][pop][0] > 0: #day 1 or zero here?
                        extinction_time = is_extinct(fish_population_log[f][pop])
                        extinction_log[f][e][pop] = extinction_time
                            #extinction_log[f].append(extinction_time)
        #
        #
        #end of evaluations loop
        #
        #
        return extinction_log, (fish_population_log, fisherman_wealth_log, price_log)
    #end evaluate function 
    
    behaviors = [0, 1,2,3,4] #0 1 2 3 4

    extinction_log = sp.zeros((len(behaviors), num_fish_species, evaluations, xsize*ysize))
    for i, b in enumerate(behaviors):
        ext_log, _ = evaluate( b )
        extinction_log[i] = ext_log
        #plot total yield in same figure? so as to maximize everything?
    extinction_log = sp.ma.masked_equal(extinction_log, 1)
    #print("\n\nRESULTS\n")
    #print("ext mean for behaviors", extinction_mean) 
    #print("ext std for behaviors", extinction_std)   


    #do we want to change extinction criterion from all dead < eps
    #to almost dead, fraction of initial suppy
    #to avoid wasting time chasing that last school of fish, or something
    
    if extinct_plot:
        #plot all the extinction points?
        extinction_mean = sp.zeros((len(behaviors),num_fish_species))
        extinction_std = sp.zeros_like(extinction_mean)
        for behav in behaviors:
            for specie in range(len(extinction_log[behav])):
                extinction_mean[behav, specie] = sp.mean(extinction_log[behav,specie])
                extinction_std[behav, specie] = sp.std(extinction_log[behav,specie])
                #print(extinction_log[behav,specie])
        
        ext_s1 = extinction_mean[:,0]
        ext_s2 = extinction_mean[:,1]
        std_s1 = extinction_std[:,0]
        std_s2 = extinction_std[:,1]
        #ext_lim_s1 = max( log[0] ) #not woeking, might want
        #print("extinct mat, s1", ext_lim_s1)
        #would probably want to reformat log
        #plt.plot( behaviors, ext_s1, linestyle='none', marker='*', color='blue')
        #plt.plot( behaviors, ext_s1 + std_s1, linestyle='none', marker='.', color='blue')
    
        plt.plot( behaviors+0.15*sp.ones_like(behaviors), ext_s2, linestyle='none', marker='*', color='green')
        plt.plot( behaviors+0.15*sp.ones_like(behaviors), ext_s2 + std_s2, linestyle='none', marker='.', color='green')
        
        for behav in behaviors:
            #for specie in range(len(extinction_log[behav])):
            for eva in range(evaluations):
                extinction_series = extinction_log[behav, 1, eva]
                plt.plot( (behav + 0.01* eva)* sp.ones_like(extinction_series), extinction_series, marker='.', linestyle='none', color='green', alpha=0.3)
 
        zero_limits()
    print("\n\nRESULTS\n")
    print("ext mean for behaviors", extinction_mean) 
    print("ext std for behaviors", extinction_std)   

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
