import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import random as rnd
#from matplotlib2tikz import save as tikz_save      #If export to tikz should be used


from fisherman import *

#I define 1 fish unit to be the maximum amount of fish that can be caugt by a standard net.
class Sea:
    #A sea consisting of tiles of fish each following a logistic growth
    #The carrying_capacity defines the capacity for all tiles, (this can be a matrix if it should differ between tiles
    #Initial population_fraction is the how large fraction of the capacity the fish will initailly be
    #Similarly the harvest rate is either a vector one for each fisherman or a scalar for all fishermans
    def __init__(self, size_tup, carrying_capacity, initial_population_fraction,g,n_fishermans,harvest_proportions,thresholds):
        self.size = size_tup
        self.growth_rate = g
        if not isinstance(carrying_capacity,list):                  #If the capacity is scalar make it a matrix
            self.carrying_capacity = sp.ones((size_tup[0],size_tup[1]))*carrying_capacity
        else:
            self.carrying_capacity = carrying_capacity
        if not isinstance(initial_population_fraction,list):        #If the initial_population_fraction is scalar make it a matrix
            initial_population_fraction = sp.ones((size_tup[0],size_tup[1]))*initial_population_fraction
        if not isinstance(harvest_proportions,list):                #If the harvest_proportions is scalar make it a matrix
            harvest_proportions= sp.ones(n_fishermans)*harvest_proportions
        if not isinstance(thresholds,list):                         #If the thresholds is scalar make it a matrix
            thresholds= sp.ones(n_fishermans)*thresholds


        #calculate the current fish population for each tile
        self.fish_population =  np.multiply(initial_population_fraction,self.carrying_capacity)

        self.fishermans_list = []
        for i in range(n_fishermans):
            x_pos = rnd.choice(range(self.size[0]))
            y_pos = rnd.choice(range(self.size[1]))
            self.fishermans_list.append(Fisherman(x_pos,self.size[0],y_pos,self.size[1],harvest_proportions[i],thresholds[i]))

    def grow(self):
        cometition_factor =  1 - np.divide(self.fish_population,self.carrying_capacity)
        population_diffence = self.growth_rate*np.multiply(cometition_factor,self.fish_population)
        self.fish_population = np.add(self.fish_population,population_diffence)
        self.fish_population = np.maximum(self.fish_population,sp.zeros((self.size[0],self.size[1])))

    def harvest(self):
        for fisherman in self.fishermans_list:  #In turns the fishermans fish
            x = fisherman.x
            y = fisherman.y
            self.fish_population[x][y] -= fisherman.throw_net(self.fish_population[x][y])

    def share_knowledge(self):  #Fisherman - Fisherman interation lies and stuff may be implemented
        ...

    def explore(self,radius,uncertainty):
        for fisherman in self.fishermans_list:  #In turns the fishermans explore a given radius
            x_to_learn = range(fisherman.x-radius,fisherman.x+radius)
            y_to_learn = range(fisherman.y-radius,fisherman.y+radius)
            for x in x_to_learn:
                x = x%self.size[0]
                for y in y_to_learn:
                    y = y%self.size[1]
                    precived_population = (1 + uncertainty*(sp.rand()-0.5))* self.fish_population[x][y]
                    fisherman.gain_knowledge(x,y,precived_population)


    def nextDay(self):
        self.grow()
        self.explore(1,0.1)
        self.harvest()


    def print(self):
        print('Fishes: ')
        print(self.fish_population)
        print('Fishermans: ')
        for fisherman in self.fishermans_list:
            type(fisherman)
            fisherman.print()



if __name__ == '__main__':
    xsize = 2
    ysize = 2
    num_fishermans = 3
    growth_rate = 0.1;
    initial_pop = 0.8;
    capacity = 1


    harvest_proportions = [0.02,0.05,0.2]
    thresholds = 1

    days = 200

    fish_population = sp.zeros((xsize*ysize,days))
    fisherman_catch = sp.zeros((num_fishermans,days))

    # Test system
    s = Sea((xsize,ysize),capacity,initial_pop,growth_rate,num_fishermans,harvest_proportions,thresholds)
    for day in range(days):
        s.nextDay()
        for i in range(num_fishermans):
            fisherman_catch[i][day] = s.fishermans_list[i].catch

        for x in range(xsize):
            for y in range(ysize):
                fish_population[x*ysize+y][day] = s.fish_population[x][y]


    #Plot the result
    plt.subplot(2,1,1)
    for i in range(xsize*ysize):
        plt.plot(sp.arange(0,days),fish_population[i],label = 'population ' + str(i+1))
    plt.ylim(0,2*capacity)
    plt.xlabel('Time')
    plt.ylabel('Fish population size')
    plt.legend()
    plt.subplot(2,1,2)
    for i in range(num_fishermans):
        plt.plot(sp.arange(0,days),fisherman_catch[i],label = 'catch ' + str(i+1))
    plt.xlabel('Time')
    plt.ylabel('Total Catch size')
    plt.legend()

    #tikz_save('modeldynamic2.tikz',        #Exporting the figure to tikz format (latex image)
    #       figureheight = '\\figureheight',
    #       figurewidth = '\\figurewidth')
    plt.show()