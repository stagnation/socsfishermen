#import matplotlib.pyplot as plt
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
    def __init__(self, size_tup, carrying_capacity, initial_population_fraction,g,n_fishermans,harvest_proportions):
        self.size = size_tup
        self.growth_rate = g
        if not isinstance(carrying_capacity,list):      #If the capacity is scalar make it a matrix
            self.carrying_capacity = sp.ones(self.size)*carrying_capacity
        else:
            self.carrying_capacity = carrying_capacity
        if not isinstance(initial_population_fraction,list):      #If the initial_population_fraction is scalar make it a matrix
            initial_population_fraction = sp.ones(self.size)*initial_population_fraction
        if not isinstance(harvest_proportions,list):      #If the capacity is scalar make it a matrix
            harvest_proportions= sp.ones(n_fishermans)*harvest_proportions

        #calculate the current fish population for each tile
        self.fish_population =  np.multiply(initial_population_fraction,self.carrying_capacity)

        self.fishermans_list = []
        for i in range(n_fishermans):
            x_pos = rnd.randint(0,self.size[0]-1)
            y_pos = rnd.randint(0,self.size[1]-1)
            self.fishermans_list.append(Fisherman(x_pos,y_pos,harvest_proportions[i],0)) #Waiting with treshold

    def grow(self):
        competition_factor =  1 - np.divide(self.fish_population,self.carrying_capacity)
        population_diffence = self.growth_rate*np.multiply(competition_factor,self.fish_population)
        self.fish_population = np.add(self.fish_population,population_diffence)
        self.fish_population = np.maximum(self.fish_population,sp.zeros(self.size))

    def harvest(self):
        for fisherman in self.fishermans_list:  #In turns the fishermans fish
            x = fisherman.x
            y = fisherman.y
            self.fish_population[x][y] -= fisherman.throw_net(self.fish_population[x][y])

    def dayDynamics(self,n_throws,flip_prob=0):
        self.grow()
        if sp.random.rand() < flip_prob:
            #flip fish populaitons and see what happens
            tmp = self.fish_population[0][0]
            self.fish_population[0][0] = self.fish_population[0][1]
            self.fish_population[0][1] = tmp
        for i in range(0,n_throws):
            self.harvest()

    def __str__(self):
        print('Fishes: ')
        print(self.fish_population)
        print('Fishermans: ')
        for fisherman in self.fishermans_list:
            type(fisherman)
            print(fisherman)
        return ""



if __name__ == '__main__':
    days = 2000
    num_of_rates = 100
    capacity = 1
    growth_rate = 0.1;
    initial_pop = 0.8;
    sailor_count = 1

    catch = sp.zeros(num_of_rates)
    maximum_catch = 0;
    maximum_harvest = 0;

    harvest_proportions = sp.arange(0,num_of_rates)/num_of_rates*2*growth_rate

    # Simulate MSY
    for k in range(num_of_rates):
        s = Sea((1,2),capacity,initial_pop,growth_rate,1,harvest_proportions[k])
        for day in range(days):
            if sp.random.rand() < 0.05:
                #randomize fisherman positions
                for f in s.fishermans_list:
                    xold = f.x
                    yold = f.y
                    f.x =rnd.randint(0,s.size[0]-1)
                    f.y =rnd.randint(0,s.size[1]-1)
                    if (xold != f.x) and (yold != f.y):
                        print(swap)
            s.dayDynamics(1)
        catch[k] = s.fishermans_list[0].catch/days
        if catch[k]>maximum_catch:
            maximum_harvest = harvest_proportions[k]
            maximum_catch = catch[k]

    #Run to find the dynamics of this population

    fish_pop_log = sp.zeros((2,days))
    s = Sea((1,2),capacity,initial_pop,growth_rate,sailor_count,maximum_harvest)
    print(s)
    #second cell, 1 _2_ is for the sheltered fish population
    #techniclly one at random of the two cells is sheltered...

    for day in range(days):
        tmp = s.fish_population
        fish_pop_log[0][day] = tmp[0][0]
        fish_pop_log[1][day] = tmp[0][1]
        s.dayDynamics(1)

    #Plot the result
    plt.subplot(2,1,1)
    if fish_pop_log[0][days-1]< fish_pop_log[1][days-1]:
        plt.plot(sp.arange(0,days),fish_pop_log[0], label='Fish dynamics at MSY')
        plt.plot(sp.arange(0,days),fish_pop_log[1], label='Fish dynamic without harvest')
    else:
        plt.plot(sp.arange(0,days),fish_pop_log[1], label='Fish dynamics at MSY')
        plt.plot(sp.arange(0,days),fish_pop_log[0], label='Fish dynamic without harvest')

    plt.ylim(0,2*capacity)
    plt.xlabel('Time')
    plt.ylabel('Fish population size')
    plt.legend()

    plt.subplot(2,1,2)
    plt.plot(harvest_proportions,catch)
    plt.ylabel('Average Catch')
    plt.xlabel('Harvest Proportion')
    #tikz_save('modeldynamic2.tikz',        #Exporting the figure to tikz format (latex image)
    #       figureheight = '\\figureheight',
    #       figurewidth = '\\figurewidth')
    plt.show()
