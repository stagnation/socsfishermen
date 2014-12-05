import scipy as sp
import numpy as np

class Fishes:
    #A sea consisting of tiles of fish each following a logistic growth
    #The carrying_capacity defines the capacity for all tiles, (this can be a matrix if it should differ between tiles
    #Initial population_fraction is the how large fraction of the capacity the fish will initailly be
    #Similarly the harvest rate is either a vector one for each fisherman or a scalar for all fishermans
    def __init__(self, initial_populations, growth_rate=0.1):
        self.growth_rate = growth_rate
        self.population =  initial_populations
        self.size = initial_populations.shape

    def grow(self,allee_effect,carrying_capacity):
        cometition_factor =  1 - np.divide(self.population, carrying_capacity)
        logistic_growth_factor = self.growth_rate*np.multiply(cometition_factor, self.population)
        allee_factor = self.population/allee_effect - 1
        population_diffence = np.multiply(logistic_growth_factor,allee_factor)
        self.population = np.add(self.population, population_diffence)
        self.population = np.maximum(self.population, sp.zeros(self.size))

    def __str__(self):
        print('Fishes: ')
        print(self.population)
        return ""
