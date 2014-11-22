import scipy as sp
import matplotlib.pyplot as plt

def discrete_trajectory(vector, allowed_directions = [(-1,0), (0,-1), (0,1), (1,0)]):
    #maximize dotproduct between allowed directions and the traj. vector
    dot_products = [ sp.dot( vector, d)  for d in allowed_directions ]
    max_idx = dot_products.index(max(dot_products))
    return allowed_directions[max_idx]
