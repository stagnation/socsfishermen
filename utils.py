import scipy as sp
import matplotlib.pyplot as plt

def discrete_trajectory(vector, allowed_directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]):
    #maximize dotproduct between allowed directions and the traj. vector
    dot_products = [ sp.dot( vector, d)  for d in allowed_directions ]
    max_idx = dot_products.index(max(dot_products))
    return allowed_directions[max_idx]

def neighborhood_tuples(x, y, side_length):
    #from -floor(side_lngth / 2) to this plus side_length
    tup_list = []
    #x_start = x - sp.floor(side_length / 2)
    #y_start = y - sp.floor(side_length / 2)
    for i in range(int(side_length)):
        for j in range(int(side_length)):
            tup_list.append( (int(x + i), int(y + j) ) )
    return tup_list
def enlarge_limits(ax=None, s=0.03):
    #courtesy of Pontus Granstrom
        if not ax:
            ax = plt.gca()
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        dx = xmax - xmin
        dy = ymax - ymin
        ax.set_xlim([xmin - s*dx, xmax + s*dx])
        ax.set_ylim([ymin - s*dy, ymax + s*dy])

def random_like(mat):
    return sp.random(mat.shape)


#def fish_sum(fishes):
#    r = 0
#    for x in range(len(fishes)):
#        for y in range(len(fishes[0]):
#            sum += fishes.population[x][y]



if __name__ == '__main__':
    #test neighbordhood_tuples:
    x = 10
    y = 10
    side_length = 3
    print(neighborhood_tuples(x, y, side_length))
