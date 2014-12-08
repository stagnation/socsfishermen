import scipy as sp
import random as rnd
from fisherman import *
from fishes import *


class Sea:
    #A sea consisting of tiles of fish each following a logistic growth
    #The carrying_capacity defines the capacity for all tiles, (this can be a matrix if it should differ between tiles
    #Initial population_fraction is the how large fraction of the capacity the fish will initailly be
    #Similarly the harvest rate is either a vector one for each fisherman or a scalar for all fishermans
    def __init__(self, size_tup = (1,1), n_fishermans = 1, harvest_fractions = 0.1, thresholds=0, greeds=0, fish_species = 1, growth_rate=0.1, initial_population_fraction = 0.5, carrying_capacity = 1, allee_effect = 0.1):
        self.size = size_tup
        if not isinstance(carrying_capacity, list):                  #If the capacity is scalar make it a matrix
            self.carrying_capacity = sp.ones(self.size)*carrying_capacity
            self.carrying_capacity = sp.tile(self.carrying_capacity,(fish_species,1,1))
        elif carrying_capacity.shape == size_tup :                   #If all fish species have same capacity
            self.carrying_capacity = sp.tile(carrying_capacity,(fish_species,1,1))
        elif carrying_capacity.shape == (fish_species,size_tup[0],size_tup[1]):
            self.carrying_capacity = carrying_capacity
        else:
            print("Error: carrying capcity is of errornus dimensions, using defult = 1")
            self.carrying_capacity = sp.ones(self.size)
            self.carrying_capacity = sp.tile(self.carrying_capacity,(fish_species,1,1))


        self.allee_effect = allee_effect

        if not isinstance(initial_population_fraction, list):        #If the initial_population_fraction is scalar make it a matrix
            initial_population_fraction = sp.ones(self.size)*initial_population_fraction
        if not isinstance(harvest_fractions, list):                #If the harvest_fractions is scalar make it a matrix
            harvest_fractions= sp.ones(n_fishermans)*harvest_fractions
        if not isinstance(thresholds, list):                         #If the thresholds is scalar make it a matrix
            thresholds= sp.ones(n_fishermans)*thresholds
        if not isinstance(greeds, list):                         #If the thresholds is scalar make it a matrix
            greeds= sp.ones(n_fishermans)*greeds

        #Initiate the fishes
        self.fishes_list = []
        for i in range(fish_species):
            self.fishes_list.append( Fishes(sp.multiply(initial_population_fraction, self.carrying_capacity[i]),growth_rate) )


        price_perceptions = sp.ones_like(self.fishes_list)
        self.fishermans_list = []
        for i in range(n_fishermans):
            x_pos = rnd.choice(range(self.size[0]))
            y_pos = rnd.choice(range(self.size[1]))
            sailor = Fisherman(x_pos, y_pos, price_perceptions, harvest_fractions[i], thresholds[i], greeds[i])
            self.fishermans_list.append(sailor)

    def harvest(self):
        for fisherman in rnd.sample(self.fishermans_list,len(self.fishermans_list)):  #In turns the fishermans fish
            #rnd.smaple to randomize order in which they fish so as to offset systematic gains for first fisherman in always fishing first
            x = fisherman.x
            y = fisherman.y
            caught = fisherman.throw_net([f.population[x][y] for f in self.fishes_list])
            for i, f in enumerate(self.fishes_list):
                f.population[x,y] -= caught[i]


    def share_knowledge(self):  #Fisherman - Fisherman interation lies and stuff may be implemented

        return None

    def explore(self, radius, uncertainty):
        for fisherman in self.fishermans_list:  #In turns the fishermans explore a given radius
            x_to_learn = range(fisherman.x-radius, fisherman.x+radius)
            y_to_learn = range(fisherman.y-radius, fisherman.y+radius)
            for x in x_to_learn:
                x = x % self.size[0]
                for y in y_to_learn:
                    y = y % self.size[1]
                    for specie, fishes in enumerate(self.fishes_list):
                        precived_population = (1 + uncertainty*(sp.rand()-0.5)) * fishes.population[x][y]
                        fisherman.gain_knowledge((x, y), precived_population, specie)

    def day_dynamics(self):
        #(fishes.grow(self.allee_effect,self.carrying_capacity) for fishes in self.fishes_list)
        for specie ,f in enumerate(self.fishes_list):
            f.grow(self.allee_effect, self.carrying_capacity[specie])
        self.explore(1, 0)
        self.harvest()

    def __str__(self):
        for fishes in self.fishes_list:
            type(fishes)
            print(fishes)
        print('Fishermans: ')
        for fisherman in self.fishermans_list:
            type(fisherman)
            print(fisherman)
        return ""
