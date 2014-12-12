#-------------------------------------------------------------------------------
# Name:         MSY
# Purpose:      Find MSY for a stationary fisherman
#
# Author:      Edvin
#
# Created:     05-12-2014
#-------------------------------------------------------------------------------

from __future__ import division
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import random as rnd
from matplotlib2tikz import save as tikz_save
from utils import *
from sea import *

if __name__ == '__main__':
    num_of_rates = 200
    days = 1000

    xsize = 1
    ysize = 1
    num_fishermans = 1
    initial_pop = 0.8
    capacity = 1
    growth_rate = 0.5
    greeds = 0
    fish_species = 1

    harvest_fractions = sp.arange(0, num_of_rates)/num_of_rates

    thresholds = 0

    catch_log = sp.zeros(num_of_rates)
    maximum_catch = 0
    maximum_harvest_fraction = 0

    for k in range(num_of_rates):
        s = Sea((xsize, ysize), num_fishermans , harvest_fractions[k] , thresholds, greeds,  fish_species, growth_rate, initial_pop, capacity)
        for day in range(days):
            s.day_dynamics()
        catch_log[k] = s.fishermans_list[0].catch[1]/days;
        if maximum_catch < catch_log[k]:
            maximum_catch = catch_log[k]
            maximum_harvest_fraction = harvest_fractions[k]
        print(k)

    #Run to find the dynamics of intresting harvest_propotions
    intrest_harvest_fractions = [0, maximum_harvest_fraction]
    days = 50
    fish_population_log = sp.zeros((4,days))
    initial_pop = 0.8
    for k in range(2):
        s = Sea((xsize, ysize), num_fishermans , intrest_harvest_fractions[k] ,  thresholds, greeds,  fish_species, growth_rate, initial_pop, capacity)
        for day in range(days):
            tmp = s.fishes_list[0].population
            fish_population_log[k][day] = tmp[0][0]
            s.day_dynamics()
    initial_pop = 0.2
    for k in range(2,4):
        s = Sea((xsize, ysize), num_fishermans , intrest_harvest_fractions[k-2] ,  thresholds, greeds,  fish_species, growth_rate, initial_pop, capacity)
        for day in range(days):
            tmp = s.fishes_list[0].population
            fish_population_log[k][day] = tmp[0][0]
            s.day_dynamics()
 #Plot the result
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(sp.arange(0, days), fish_population_log[0], 'b', label='Fish dynamics at no harvest')
    ax1.plot(sp.arange(0, days), fish_population_log[1], 'g', label='Fish dynamics at MSY')
    ax1.plot(sp.arange(0, days), fish_population_log[2], 'b')
    ax1.plot(sp.arange(0, days), fish_population_log[3], 'g')
    ax1.set_ylim(0, 2*capacity)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Fish population size')
    plt.legend()
    enlarge_limits(ax1)

    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(harvest_fractions,catch_log)
    ax2.set_ylabel('Average Catch')
    ax2.set_xlabel('Harvest fraction')
    tikz_save('modeldynamic2.tikz',        #Exporting the figure to tikz format (latex image)
           figureheight = '\\figureheight',
           figurewidth = '\\figurewidth')
    enlarge_limits()
    #plt.savefig("figs/example_figure %s %s %s.png" %(days, num_of_rates, sailor_count), bbox_inches='tight')
    plt.show()
