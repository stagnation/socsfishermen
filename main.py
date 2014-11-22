from fish import *
from people import *
from sea import *
from utils import *
from random import choice
import matplotlib.pyplot as plt
import scipy as sp


def print_people(people_list, mat_size):
    mat = sp.zeros( shape=mat_size )
    for i, p in enumerate(people_list):
        mat[p.x, p.y] = i+1
    print(mat)

def move_fishes(sea):
    #Modified diffusion model to make sure only one fish is on same location
    for f in sea.fish_list:
        directions = [(-1,0), (0,-1), (0,1), (1,0)]
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

    #make sure there is fish here
    if not isinstance(fish, Fish):
        print("No fish at %s, %s" % (person.x, person.y ))
        return 0
    greed = person.threshhold
    tot_catch = 0
    print("before throwing nets")
    print(person)
    print(fish)
    while tot_catch < greed:
        catch = fish.fish_caught()
        tot_catch += catch
        if catch == 0: #if one nets yield nothing, the fishing is done
            break
    person.catch = tot_catch
    print("-->", person)
    print(fish)
    #fish_caught method returns number of fish caught in each net
    #fish_caught should accurately reduce the number of fish.
    return 0


def move_to_site(people_list):
    #person has decided upon a site with roghly X fish
    #person want to maximize his yield, if he finds a spot on his way
    #with more than X he stops and fishe sthere.
    #also if another fisher is nearby he has to split
    #and might want to go somewhere else instead.

    #should be in lockstep, all people move one step, check if they are too close
    #and adjust their course accordingly

    for i in range(100): #shoul be a clever while, poss do-while
        #print("step %s" % (i) )
        for p in people_list:
            trajectory = (p.target_x - p.x, p.target_y - p.y)
            #ignroe directions if there are fishermen there - later on let
            #this ignore field be larger and dependent on fish to people ration
            #in the area
            trajectory = discrete_trajectory(trajectory)
            #print(trajectory)
            p.x = p.x + trajectory[0]
            p.y = p.y + trajectory[1]

            if (p.x == p.target_y) and (p.y == p.target_y):
                #print("person at target %s, %s" % (p.x, p.y) )
                break #this doesn't break properly

    return 0

if __name__ == '__main__':
    print('starting --\n')
    sea_size=(3,3)
    s = Sea(sea_size,9,100)
    s.print_fish()
    move_fishes(s)
    s.print_fish()
    p = People(0,0,4)
    p.target_x = 1
    p.target_y = 1
    people_list = [p]
    move_to_site(people_list)
    for p in people_list:
        throw_net(p, s.grid[p.x][p.y])
    print_people(people_list, sea_size)

