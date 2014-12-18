from fishermanEconomic import *
import scipy as sp

def adapt(fisherman_list):
    #Is neighbour fisherman better? 1d neigbour torus
    if sp.rand()>1e-1:
        return
    n_fishermans = fisherman_list.__len__()
    prev = n_fishermans - 1
    uppdate_list = [0 for x in range(n_fishermans)]
    #Find out which neighbour is best
    for cur, fisherman in enumerate(fisherman_list):
        next = (cur + 1)%n_fishermans
        best = sp.argmax([fisherman_list[prev].moneyDiff(),fisherman.moneyDiff(),fisherman_list[next].moneyDiff()])
        if best == 0:
            uppdate_list[cur] = prev
        elif best == 1:
            uppdate_list[cur] = cur
        else:
            uppdate_list[cur] = next
        prev = cur

    #Update & evolve new strategies

    for cur, fisherman in enumerate(fisherman_list):

        if sp.rand()>1e-2:
            fisherman.greed = fisherman_list[uppdate_list[cur]].greed
        else:
            fisherman.greed += 5e-1*(sp.rand()-0.5)
            fisherman.greed *= fisherman.greed>0


    #Evolve new strategies