import scipy as sp
import random as rnd
from fishermanEconomic import *
from fisherman import *
from fishes import *


class Sea:
    #A sea consisting of tiles of fish each following a logistic growth
    #The carrying_capacity defines the capacity for all tiles, (this can be a matrix if it should differ between tiles
    #Initial population_fraction is the how large fraction of the capacity the fish will initailly be
    #Similarly the harvest rate is either a vector one for each fisherman or a scalar for all fishermans
    def __init__(self, size_tup, n_fishermans, harvest_fractions, thresholds, greeds, fish_species, growth_rate, initial_population_fraction, carrying_capacity, allee_effect, fisher_behavior,varyharvest =False):
        self.fisher_behavior = fisher_behavior
        self.size = size_tup
        if not isinstance(carrying_capacity, list):                  #If the capacity is scalar make it a matrix
            self.carrying_capacity = sp.ones(self.size)*carrying_capacity
            self.carrying_capacity = sp.tile(self.carrying_capacity,(fish_species,1,1))
        elif len(carrying_capacity) != fish_species:
        #carrying_capacity.shape == size_tup :                   #If all fish species have same capacity
            self.carrying_capacity = sp.tile(carrying_capacity,(fish_species,1,1))
        elif carrying_capacity[0].shape == (size_tup[0],size_tup[1]):
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
            if varyharvest:
                sailor = FishermanVaryHarvest(x_pos, y_pos, price_perceptions, harvest_fractions[i], thresholds[i], greeds[i])
            else:
                sailor = Fisherman(x_pos, y_pos, price_perceptions, harvest_fractions[i], thresholds[i], greeds[i])
            self.fishermans_list.append(sailor)

    def harvest(self):
        for fisherman in rnd.sample(self.fishermans_list,len(self.fishermans_list)):  #In turns the fishermans fish
            #fisherman.move_to_best() handled in day dynamics
            #rnd.smaple to randomize order in which they fish so as to offset systematic gains for first fisherman in always fishing first
            x = fisherman.x
            y = fisherman.y
            caught = fisherman.throw_net([f.population[x,y] for f in self.fishes_list])
            for i, f in enumerate(self.fishes_list):
                f.population[x,y] -= caught[i]


    def share_knowledge(self):  #Fisherman - Fisherman interation lies and stuff may be implemented

        return None

    def explore_all(self, radius, uncertainty):
        for fisherman in self.fishermans_list:  #In turns the fishermans explore a given radius
            self.explore(fisherman, radius, uncertainty)

    def explore(self, fisherman, radius, uncertainty):
            x_to_learn = range(fisherman.x-radius, fisherman.x+radius)
            y_to_learn = range(fisherman.y-radius, fisherman.y+radius)
            for x in x_to_learn:
                x = x % self.size[0]
                for y in y_to_learn:
                    y = y % self.size[1]
                    for specie, fishes in enumerate(self.fishes_list):
                        precived_population = (1 + uncertainty*(sp.rand()-0.5)) * fishes.population[x,y]
                        fisherman.gain_knowledge((x, y), precived_population, specie)

    def day_dynamics(self):
        #(fishes.grow(self.allee_effect,self.carrying_capacity) for fishes in self.fishes_list)
        for specie ,f in enumerate(self.fishes_list):
            survive = f.grow(self.carrying_capacity[specie], self.allee_effect) #returns true while fishes are still alive, false if extinct
            #if not survive:
            #    print("sea extinct")
            #    return False #when first species goes extinct, todo: all species but one or something?
        self.explore_all(1, 0)

        if self.fisher_behavior == 0: #don't move until fish is extinct
            for f in self.fishermans_list:
                location = f.current_fishing_tactic[0]
                specie = f.current_fishing_tactic[1]
                if self.fishes_list[specie].population[location] == 0:
                    f.move_to_best()

        if self.fisher_behavior == 1: #move each day
            for f in self.fishermans_list:
                f.move_to_best()

        if self.fisher_behavior == 2: #move each day + no return
            for f in self.fishermans_list:
                current_pos = f.current_fishing_tactic
                best = f.move_to_best()
                if best == current_pos:
                    f.perception_of_fishpopulation_value.remove(best)
                    f.move_to_best()

        if self.fisher_behavior == 3: #move each day + large radius
            for f in self.fishermans_list:
                self.explore(f, 2, 0)
                f.move_to_best()

        if self.fisher_behavior == 4: #move each day + no return + large radius
            for f in self.fishermans_list:
                current_pos = f.current_fishing_tactic
                self.explore(f, 2, 0)
                best = f.move_to_best()
                if best == current_pos:
                    f.perception_of_fishpopulation_value.remove(best)
                    f.move_to_best()

        self.harvest()

        #do we want diffusion?
        #for f in self.fishes_list:
        #    f.diffuse()
        return True

    def __str__(self):
        for fishes in self.fishes_list:
            type(fishes)
            print(fishes)
        print('Fishermans: ')
        for fisherman in self.fishermans_list:
            type(fisherman)
            print(fisherman)
        print("carry", self.carrying_capacity)
        print("********")
        print("params: ")
        print("size", self.size)
        print("num sail", len(self.fishermans_list))
        print("harvest", [f.harvest_fraction for f in self.fishermans_list])
        print("threshold", [f.threshold for f in self.fishermans_list])
        print("greeds", [f.greed for f in self.fishermans_list])
        print("fish s", len(self.fishes_list))
        print("g rate", [f.growth_rate for f in self.fishes_list])
        #print("pop0", self.initial_population_fraction)

        print("allee", self.allee_effect)



        return ""



