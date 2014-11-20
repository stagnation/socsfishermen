from fish import *
from random import choice
from people import *
import matplotlib.pyplot as plt
import scipy as sp

class Sea:
    #lookup matrix/dict representation of the fishes

    def __init__(self, size_tup, fish_initial_count, population_total):
        self.size = size_tup
        self.grid = [ [ 0  for x in range(size_tup[1]) ] for y in range(size_tup[0]) ]
        #exchange 0 for empty lsit or data struct for easy add/rem of objects
        self.fish_list = []
        remaining_fish = population_total
        rand_dist  = sp.random.rand(fish_initial_count)
        fish_dist = rand_dist / sum(rand_dist) * population_total

        for i in range(fish_initial_count):
            fish_x = sp.random.randint(size_tup[0])
            fish_y = sp.random.randint(size_tup[1])
            #random fish_size
            fish_number = int(fish_dist[i])
            remaining_fish -= fish_number
            #add fisg to list and grid representation
            if isinstance(self.grid[fish_x][fish_y], Fish):
                #handle this better, a list of all schools is prob better
                self.grid[fish_x][fish_y].add(fish_number)
            else:
                fish = Fish( fish_x, fish_y, fish_number )
                print(fish.count)
                self.fish_list.append(fish)
                self.grid[fish_x][fish_y] = fish
        self.grid[fish_x][fish_y].add(remaining_fish)
    def to_mat(self):
        mat = sp.zeros( shape=self.size )
        for f in self.fish_list:
            x = f.x
            y = f.y
            v = f.count
            print(v)
            mat[x,y] = v
        return mat

def move_fishes(sea):
    #Modified diffusion model to make sure only one fish is on same location
    for f in sea.fish_list:
        directions = [(-1,0), (0,-1), (0,1), (0,1)]
        while True:
            if len(directions) == 0:
                pos = (f.x, f.y)
                break
            delta = choice(directions)
            pos = ((f.x + delta[0]) % sea.size[0], (f.y + delta[1]) % sea.size[1])
            if not isinstance(sea.grid[pos[0]][pos[1]], Fish):
                break;
            directions.remove(delta)

        sea.grid[f.x][f.y] = 0
        f.x = pos[0]
        f.y = pos[1]
        sea.grid[f.x][f.y] = f

def throw_net(person, fish):
    #person would fish until some threshold or heurestic is fulfilled
    #upon each throw of net a fraction of the fish population would be removed
    #and added to his catch
    return 0

if __name__ == '__main__':
    print('test')
    s = Sea((3,3),3,10)
    m = s.to_mat()
    print(m)
    move_fishes(s)
    print(s.to_mat())
