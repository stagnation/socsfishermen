import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import random as rnd
from utils import *
#from matplotlib2tikz import save as tikz_save      #If export to tikz should be used

from sea import *

if __name__ == '__main__':
    xsize = 1
    ysize = 3
    num_fishermans = 1
    initial_pop = 0.8
    capacity = 1
    allee_effect = 0.1;
    growth_rate = 1*allee_effect

    harvest_fractions = [0.2]
    thresholds = 0.04

    days = 200

    fish_population_log = sp.zeros((xsize*ysize, days))
    fisherman_catch_log = sp.zeros((num_fishermans, days))
    # Test system
    s = Sea((xsize, ysize), num_fishermans, harvest_fractions , thresholds)
    #Below is the defult vaules
    #Sea(size_tup = (1,1), num_fishermans = 1, harvest_fractions = 0.2, thresholds=0, growth_rate=0.1, initial_population_fraction = 0.5, carrying_capacity = 1, allee_effect = 0.1)
    for day in range(days):
        s.day_dynamics()
        for i in range(num_fishermans):
            fisherman_catch_log[i][day] = s.fishermans_list[i].catch

        for x in range(xsize):
            for y in range(ysize):
                fish_population_log[x*ysize+y][day] = s.fishes.population[x][y]


    #Plot the result
    ax1 = plt.subplot(2, 1, 1)
    for i in range(xsize*ysize):
        ax1.plot(sp.arange(0, days), fish_population_log[i], label = 'population ' + str(i+1))
    ax1.set_ylim(0, 2*capacity)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Fish population size')
    plt.legend()
    ax2 = plt.subplot(2, 1, 2)
    for i in range(num_fishermans):
        ax2.plot(sp.arange(0, days), fisherman_catch_log[i], label = 'catch' + str(i+1))
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Total Catch size')
    plt.legend()

    #tikz_save('modeldynamic2.tikz',        #Exporting the figure to tikz format (latex image)
    #       figureheight = '\\figureheight',
    #       figurewidth = '\\figurewidth')
    enlarge_limits(ax1)
    enlarge_limits(ax2)
    plt.show()
