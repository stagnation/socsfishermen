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
        print("No fish found for  %s, %s" % (person.x, person.y ))
        return 0
    greed = person.threshhold - person.catch
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
            if (p.x == p.target_y) and (p.y == p.target_y):
                #print("person at target %s, %s" % (p.x, p.y) )
                break #this doesn't break properly
                #could have two lists, one with all people, for collison
                #checks and one with movable people
                #Once on has reached target can remve from movavle

            trajectory = (p.target_x - p.x, p.target_y - p.y)
            #ignroe directions if there are fishermen there - later on let
            #this ignore field be larger and dependent on fish to people ration
            #in the area
            trajectory = discrete_trajectory(trajectory)
            #print(trajectory)
            p.x = p.x + trajectory[0]
            p.y = p.y + trajectory[1]


    return 0

def survey_fish_grid_neighborhood(person, sea):
    #person have already moved to a fishing site on the coarse people grid
    #the fish grid is more fine and more than one fish grid cell could
    #be available for a given fishing site.
    #want to survey all/some of the of the cells and select the best.
    fish_x = person.x * sea.grid_scaling_factor
    fish_y = person.y * sea.grid_scaling_factor
    fishing_locations_fishgrid = neighborhood_tuples(fish_x, fish_y, sea.grid_scaling_factor)
    #Look at all the fishes
    available_fishes = [ sea.grid[d[0]][d[1]] for d in fishing_locations_fishgrid ]
    available_fishes = [ f for f in available_fishes if isinstance(f, Fish) ]
    print(available_fishes)
    #and find the best
    def find_best_fish(fish_list):
        if fish_list == []:
            return 1
        available_count = [ f.count for f in available_fishes ]
        best_fish_idx = available_count.index(max(available_count))
        return fish_list[best_fish_idx]

    best_fish = find_best_fish(available_fishes)
    #what if there are no fish here?
    if not isinstance(best_fish, Fish):
        return 0
    print("best fish available in site %s, %s, with %s count" %(person.x, person.y, best_fish.count) )
    throw_net( person, best_fish )




    #other solutions is to sort them from best to worst.
    #find the first couple of "good enough" fishes
    #either in the full cell or along a given search path stattin from
    #the middle - this would be the most realistic.

    #the result of this survey should probably be saved in the fisherman's memory
    #so this can be done only once per cell if he returns often
    #and so method calls following this can know whcih fishes he is
    #Interested in interacting with


if __name__ == '__main__':
    print('starting --\n')
    #INIT
    sea_size=(6,6)
    people_grid_size=(3,3)
    s = Sea(sea_size,30,10000)
    s.grid_scaling_factor = sea_size[0] / people_grid_size[0]
    p = People(0,0,4)
    p.target_x = 1
    p.target_y = 1
    people_list = [p]
    day_count = 10
    fish_population_size = sp.zeros(day_count)
    #i = 1. #to be replaced with a for loop
    for i in range(day_count):
        #FIRST NIGHT - fish move
        move_fishes(s)
        s.print_fish()
        #FIRST DAY - people move and fish
        move_to_site(people_list)
        #reset people to dock position, and 0 catch
        for p in people_list:
            if p.catch < p.threshhold:
                #+reevaluate target
                p.target_x = sp.random.randint(people_grid_size[0])
                p.target_y = sp.random.randint(people_grid_size[1])
                #make sure not same target as before?

            p.x = 0
            p.y = 0
            p.catch = 0
        for p in people_list:
            survey_fish_grid_neighborhood(p, s)
            #throw_net(p, s.grid[p.x][p.y])
        print_people(people_list, people_grid_size)
        fish_population_size[i] = s.fish_population_size()

    print(fish_population_size)
