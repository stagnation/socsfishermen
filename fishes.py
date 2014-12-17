import scipy as sp
import random as ran

class Fishes:
    #A sea consisting of tiles of fish each following a logistic growth
    #The carrying_capacity defines the capacity for all tiles, (this can be a matrix if it should differ between tiles
    #Initial population_fraction is the how large fraction of the capacity the fish will initailly be
    #Similarly the harvest rate is either a vector one for each fisherman or a scalar for all fishermans

    def __init__(self, initial_populations, growth_rate):
        self.growth_rate = growth_rate
        self.population =  initial_populations
        self.size = initial_populations.shape

    def grow(self,carrying_capacity, allee):
        cometition_factor =  1 - sp.divide(self.population, carrying_capacity)
        self.population += self.growth_rate*sp.multiply(self.population,cometition_factor)# Logistic growth
        #self.population = self.population * sp.exp( self.growth_rate*cometition_factor)#ricker
        self.population = sp.maximum(self.population, sp.zeros(self.size))

        #Numerical errors trying to compensate...
        extinction_limit = 1e-3
        survive_matrix = (self.population>extinction_limit)
        self.population = self.population * survive_matrix
        if not sp.any(survive_matrix):
            print("all extinct")
            return False
        return True

    def diffuse(self):
        diffusion = 0.1
        x = sp.random.randint(self.size[0])
        y = sp.random.randint(self.size[1])
        directions = [((x -1) % self.size[0],y% self.size[1]), (x% self.size[0], (y-1)% self.size[1]), (x% self.size[0],(y+1)% self.size[1]), ((x+1)% self.size[0],y% self.size[1])]
        avail = [ d for d in directions if self.population[d] == 0]
        if avail:
            newpos = ran.choice( avail )
            self.population[newpos] = diffusion * self.population[x,y]
            self.population[x,y] -= diffusion * self.population[x,y]



    def __str__(self):
        print('Fishes: ')
        print(self.population)
        return ""
