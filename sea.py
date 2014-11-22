from random import choice
import matplotlib.pyplot as plt
import scipy as sp
from fish import *
from people import *

class Sea:
    #lookup matrix/dict representation of the fishes

    def __init__(self, size_tup, fish_initial_count, population_total):
        self.size = size_tup
        self.grid = [ [ 0  for x in range(size_tup[1]) ] for y in range(size_tup[0]) ]
        #exchange 0 for empty lsit or data struct for easy add/rem of objects
        self.fish_list = []
        remaining_fish = population_total
        for i in range(fish_initial_count):
            fish_x = sp.random.randint(size_tup[0])
            fish_y = sp.random.randint(size_tup[1])
            #random fish_size
            fish_number = remaining_fish / ( fish_initial_count - i) * 2 * sp.random.rand()
            remaining_fish -= fish_number
            #add fisg to list and grid representation
            if isinstance(self.grid[fish_x][fish_y], Fish):
                #handle this better, a list of all schools is prob better
                self.grid[fish_x][fish_y].add(fish_number)
            else:
                fish = Fish( fish_x, fish_y, fish_number )
                #print(fish.count)
                self.fish_list.append(fish)
                self.grid[fish_x][fish_y] = fish

    def to_mat(self):
        mat = sp.zeros( shape=self.size )
        for f in self.fish_list:
            x = f.x
            y = f.y
            v = f.count
            mat[x,y] = v
        return mat
    def print_fish(self):
        mat = self.to_mat()
        print(mat)
