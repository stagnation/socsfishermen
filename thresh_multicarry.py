import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy as sp
import numpy as np
import random as rnd
from utils import *
#from matplotlib2tikz import save as tikz_save      #If export to tikz should be used

from sea import *

if __name__ == '__main__':
    xsize = 3
    ysize = 3
    num_fishermans = 3
    initial_pop = 0.5
    capacity = 1
    cap_mat = capacity * sp.ones((xsize,ysize))
    cap_mat += 0.1 * ( sp.random.random(cap_mat.shape) - 0.5 )
    cap_mat[0,0] = 2
    allee_effect = 0.1;
    growth_rate = 0.8

    harvest_fractions = 0.2
    thresholds = 0.037

    days = 200

    fish_population_log = sp.zeros((xsize*ysize, days))
    fisherman_totalcatch_log = sp.zeros((num_fishermans, days))
    fisherman_pos_log = sp.zeros((num_fishermans,2, days))
    fisherman_dailycatch_log = sp.zeros((num_fishermans, days))
    # Test system
    s = Sea((xsize, ysize), num_fishermans, harvest_fractions , thresholds, growth_rate, initial_pop, cap_mat, allee_effect)
    #Below is the defult vaules
    #Sea(size_tup = (1,1), num_fishermans = 1, harvest_fractions = 0.2, thresholds=0, growth_rate=0.1, initial_population_fraction = 0.5, carrying_capacity = 1, allee_effect = 0.1)
    for day in range(days):
        s.day_dynamics()
        for i in range(num_fishermans):
            fisherman_totalcatch_log[i][day] = s.fishermans_list[i].catch
            fisherman_dailycatch_log[i][day] = s.fishermans_list[i].catch - fisherman_totalcatch_log[i][day-1] if day > 0 else s.fishermans_list[i].catch
            fisherman_pos_log[i, 0, day] = s.fishermans_list[i].x
            fisherman_pos_log[i, 1, day] = s.fishermans_list[i].y

        for x in range(xsize):
            for y in range(ysize):
                fish_population_log[x*ysize+y][day] = s.fishes.population[x][y]


    #Plot the result
    num_subplots = 3
    subplot_num = 0
    subplot_num+=1
    ax1 = plt.subplot(num_subplots, 1, subplot_num)
    for i in range(xsize*ysize):
        ax1.plot(sp.arange(0, days), fish_population_log[i], label = 'population ' + str(i+1))
    ax1.set_ylim(0, 2*capacity)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Fish population size')
    plt.legend()
    subplot_num+=1
    ax2 = plt.subplot(num_subplots, 1, subplot_num)
    for i in range(num_fishermans):
        #ax2.plot(sp.arange(0, days), fisherman_totalcatch_log[i], label = 'catch' + str(i+1))
        ax2.plot(range(days), days*fisherman_dailycatch_log[i])
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Total Catch size')
    plt.legend()
    
    subplot_num+=1
    ax3 = plt.subplot(num_subplots, 1, subplot_num)
    for i in range(num_fishermans):
        ax3.plot( fisherman_pos_log[i,0,:],  fisherman_pos_log[i,1,:])
    

    #tikz_save('modeldynamic2.tikz',        #Exporting the figure to tikz format (latex image)
    #       figureheight = '\\figureheight',
    #       figurewidth = '\\figurewidth')
    enlarge_limits(ax1)
    enlarge_limits(ax2)
    plt.show()
