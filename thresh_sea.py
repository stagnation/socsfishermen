import scipy as sp
import numpy as np
import random as rnd
from fisherman import *
from fishes import *

class Sea:
    #A sea consisting of tiles of fish each following a logistic growth
    #The carrying_capacity defines the capacity for all tiles, (this can be a matrix if it should differ between tiles
    #Initial population_fraction is the how large fraction of the capacity the fish will initailly be
    #Similarly the harvest rate is either a vector one for each fisherman or a scalar for all fishermans
    def __init__(self, size_tup = (1,1), n_fishermans = 1, harvest_fractions = 0.1, thresholds=0, growth_rate=0.1, initial_population_fraction = 0.5, carrying_capacity = 1, allee_effect = 0.1):
        self.size = size_tup
        if not isinstance(carrying_capacity, list):                  #If the capacity is scalar make it a matrix
            self.carrying_capacity = sp.ones(self.size)*carrying_capacity
        else:
            self.carrying_capacity = carrying_capacity

        self.allee_effect = allee_effect

        if not isinstance(initial_population_fraction, list):        #If the initial_population_fraction is scalar make it a matrix
            initial_population_fraction = sp.ones(self.size)*initial_population_fraction
        if not isinstance(harvest_fractions, list):                #If the harvest_fractions is scalar make it a matrix
            harvest_fractions= sp.ones(n_fishermans)*harvest_fractions
        if not isinstance(thresholds, list):                         #If the thresholds is scalar make it a matrix
            thresholds= sp.ones(n_fishermans)*thresholds

        #Initiate the fishes
        self.fishes =  Fishes(np.multiply(initial_population_fraction, self.carrying_capacity),growth_rate)

        self.fishermans_list = []
        for i in range(n_fishermans):
            x_pos = rnd.choice(range(self.size[0]))
            y_pos = rnd.choice(range(self.size[1]))
            sailor = Fisherman(x_pos, y_pos, harvest_fractions[i], thresholds[i])
            self.fishermans_list.append(sailor)

    def harvest(self):
        for fisherman in self.fishermans_list:  #In turns the fishermans fish
            x = fisherman.x
            y = fisherman.y
            self.fishes.population[x][y] -= fisherman.throw_net(self.fishes.population[x][y])

    def share_knowledge(self):  #Fisherman - Fisherman interation lies and stuff may be implemented

        return None

    def explore(self, radius, uncertainty):
        for fisherman in self.fishermans_list:  #In turns the fishermans explore a given radius
            x_to_learn = range(fisherman.x-radius, fisherman.x+radius)
            y_to_learn = range(fisherman.y-radius, fisherman.y+radius)
            for x in x_to_learn:
                x = x%self.size[0]
                for y in y_to_learn:
                    y = y%self.size[1]
                    precived_population = (1 + uncertainty*(sp.rand()-0.5))*self.fishes.population[x][y]
                    fisherman.gain_knowledge(x, y, precived_population)


    def day_dynamics(self):
        self.fishes.grow(self.allee_effect,self.carrying_capacity)
        self.explore(1, 0.1)
        self.harvest()

    def __str__(self):
        self.fishes.__str__()
        print('Fishermans: ')
        for fisherman in self.fishermans_list:
            type(fisherman)
            print(fisherman)
        return ""
