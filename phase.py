import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy as sp
import numpy as np
import random as rnd
from utils import *
from scipy import vectorize
#from matplotlib2tikz import save as tikz_save      #If export to tikz should be used

from sea import *

if __name__ == '__main__':
    xsize = 1
    ysize = 2
    num_fishermans = 1
    fish_species = 1
    greeds = 0
    initial_pop = 0.5
    capacity = 1
    cap_mat = capacity * sp.ones((xsize,ysize))
    cap_mat += 0.1 * ( sp.random.random(cap_mat.shape) - 0.5 )
    cap_mat[0,0] = 2
    allee_effect = 0.1;
    allees = sp.linspace(0.1,0.2,10)
    growth_rate = 1

    harvest_fractions = sp.linspace(0,0.5,10)
    thresholds = sp.linspace(0,0.1,100)
    res = sp.zeros((len(allees), len(harvest_fractions), len(thresholds), 2))
    days = 20

    fish_population_log = sp.zeros((xsize*ysize, days))
    growth_rate = 1
    #for a, allee in enumerate(allees):
    #    for h, harvest in enumerate(harvest_fractions):
     #       for t, threshold in enumerate(thresholds):
    #            print(a,h,t)
      #          # Test system
       #         growth = growth_rate * allee
      #          s = Sea((xsize, ysize), num_fishermans, harvest, threshold, growth, initial_pop, capacity, allee)
                #Below is the defult vaules
                #Sea(size_tup = (1,1), num_fishermans = 1, harvest_fractions = 0.2, thresholds=0, growth_rate=0.1, initial_population_fraction =                0.5, carrying_capacity = 1, allee_effect = 0.1)
       #         for day in range(days):
       #             s.day_dynamics()
       #         res[a, h, t, 0] = s.fishes.population.sum()
       #         res[a, h, t, 1] = sum( f.catch for f in s.fishermans_list )


    #In lieu of loop over allee
    #res = [ 0 for a in allees]
    a = 0
    allee = 0.1
    @vectorize
    def innerloop(allee, harvest, threshold):
        # Test system
        s = Sea((xsize, ysize), num_fishermans, harvest, threshold, greeds, fish_species, growth_rate, initial_pop, capacity, allee)
        for day in range(days):
            s.day_dynamics()
        return s.fishes_list[0].population.sum(), sum( f.catch[1] for f in s.fishermans_list )


    harvestmat, thresholdmat = sp.meshgrid(harvest_fractions, thresholds)
    res = innerloop(allee, harvestmat, thresholdmat)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(harvestmat, thresholdmat, res[a], rstride=1, cstride=1, cmap=plt.cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_xlabel("harvest rate")
    ax.set_ylabel("threshold")
    ax.set_zlabel("final fish population")
    plt.show()



    #Plot the result

    #tikz_save('modeldynamic2.tikz',        #Exporting the figure to tikz format (latex image)
    #       figureheight = '\\figureheight',
    #       figurewidth = '\\figurewidth')
