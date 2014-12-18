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
    def __init__(self, size_tup, n_fishermans, harvest_fractions, thresholds, greeds, fish_species, growth_rate, initial_population_fraction, carrying_capacity, allee_effect, fisher_behavior, varyharvest, levels):
        self.fisher_behavior = fisher_behavior
        self.size = size_tup
        self.diffuse = False
        self.truncate_extinction = True
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

        #Initiate fishermen
        price_perceptions = sp.ones_like(self.fishes_list)
        self.fishermans_list = []
        for i in range(n_fishermans):
            x_pos = rnd.choice(range(self.size[0]))
            y_pos = rnd.choice(range(self.size[1]))
            if varyharvest:
                sailor = FishermanVaryHarvest(x_pos, y_pos, price_perceptions, harvest_fractions[i], thresholds[i], greeds[i], levels[i])
            else:
                sailor =            Fisherman(x_pos, y_pos, price_perceptions, harvest_fractions[i], thresholds[i], greeds[i], levels[i]) #prob no level
            self.fishermans_list.append(sailor)
        self.num_zero_levels = len(levels) - sum(levels)

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

    def explore_everyone(self, radius, uncertainty):
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
                        
#finds the nth best location for each fish specie                        
    def explore_nth_best(self, fisherman, one_level_num, blacklist=[]):
        #nth best 0 indexed, 0 is best-best, 1 is second best and so on.
        #blacklsit if we want l1 fishermans to explicitly ignore where l0 fishermen are
        nth_best = self.num_zero_levels + one_level_num
        for s, fish_mat in enumerate(self.fishes_list):
            rav = sp.ravel(fish_mat) #mask with blacklist if applicable
            nth_best_idx = len(rav) - nth_best
            rav_idx = sp.where(rav==nth_best_idx)[0][0]
            location = sp.unravel_index(rav_idx, fishes_mat.shape)
            fisherman.gain_knowledge(location, fish_mat[location], s)
            
#finds the best available location for each specie            
    def explore_best_remaining(self, fisherman, blacklist):
        #I WANT:
        #blacklist: list of locations
        #blacklist[specie] = list[ (x,y), (x,y), (x,y)]
        
        #EASY TO GET:
        #blacklist: list of tactics
        #blacklist = list[ (s, (x,y)), (s, (x,y)) ...]
        for s, fishes in enumerate(self.fishes_list):
            fish_mat = fishes.population
            mask = sp.ones_like(fish_mat)
            for loc in blacklist[s]: #blacklist[]s:
                mask[loc] = 0
            mask_mat = sp.ma.masked_array(fish_mat, mask)
            location = mask_mat.argmax()
            location = sp.unravel_index(location, fish_mat.shape)
            fisherman.gain_knowledge(location, fish_mat[location], s)


    def day_dynamics(self):
        #(fishes.grow(self.allee_effect,self.carrying_capacity) for fishes in self.fishes_list)
        for specie ,f in enumerate(self.fishes_list):
            survive = f.grow(self.carrying_capacity[specie], self.allee_effect) #returns true while fishes are still alive, false if extinct
            if not survive and self.truncate_extinction:
                #print("sea extinct")
                return False #when first species goes extinct, todo: all species but one or something?

        #want to know how many 0-levels
        #and count up the 1-levels
        
        fisherman_locations = [[ (None,)*2 for i in range(len(self.fishermans_list))] for x in range(len(self.fishes_list))]
        #refactor to have two lists with num_Fiserman nones and
        #add a few elements to them so they are sorted by species....
        
        for fidx, f in enumerate(self.fishermans_list):  #would be easier if the one levels are always alst here
            if f.level == 0:
                if self.fisher_behavior == 0: #don't move until fish is extinct
                    location = f.current_fishing_tactic[0]
                    specie = f.current_fishing_tactic[1]
                    if self.fishes_list[specie].population[location] == 0:
                        self.explore(f, 1, 0)
                        f.move_to_best()

                if self.fisher_behavior == 1: #move each day
                    self.explore(f, 1, 0)
                    f.move_to_best()

                if self.fisher_behavior == 2: #move each day + no return
                    current_pos = f.current_fishing_tactic
                    self.explore(f, 1, 0)
                    best = f.move_to_best()
                    if best == current_pos:
                        f.perception_of_fishpopulation_value.remove(best)
                        f.move_to_best()

                #if self.fisher_behavior == 3: #move each day + large radius
                #    self.explore(f, 2, 0)
                #    f.move_to_best()

                #if self.fisher_behavior == 4: #move each day + no return + large radius
                #    current_pos = f.current_fishing_tactic
                #    self.explore(f, 2, 0)
                #    best = f.move_to_best()
                #    if best == current_pos:
                #        f.perception_of_fishpopulation_value.remove(best)
                #        f.move_to_best()
                        
                tactic = f.current_fishing_tactic
                specie = tactic[1]
                location = tactic[0]
                fisherman_locations[specie][fidx] = location        
                        
        for fidx, f in enumerate(self.fishermans_list):       #quick and dirty solution-...          
            if f.level == 1:
                f.perception_of_fishpopulation_value = [] #[((x,y),0,0)]
                self.explore_best_remaining(f, fisherman_locations)
                f.move_to_best()

                tactic = f.current_fishing_tactic
                specie = tactic[1]
                location = tactic[0]
                fisherman_locations[specie][fidx] = location
                
                #not sure if this movemnet works properly or if it just makes everything much more resilient...
                
        #end fisherman loop    

        self.harvest()

        #do we want diffusion?
        if self.diffuse:
            for f in self.fishes_list:
                f.diffuse()
                
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




