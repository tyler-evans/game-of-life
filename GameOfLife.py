import numpy as np
from numpy import uint8

# Shift the state matrix north, filling in the south row with zeros
def north(state):
    state = np.roll(state, -1, axis=0)
    state[-1,:] = 0
    return state

# Shift the state matrix south, filling in the north row with zeros
def south(state):
    state = np.roll(state, 1, axis=0)
    state[0,:] = 0
    return state

# Shift the state matrix west, filling in the east col with zeros
def west(state):
    state = np.roll(state, -1, axis=1)
    state[:,-1] = 0
    return state

# Shift the state matrix east, filling in the west col with zeros
def east(state):
    state = np.roll(state, 1, axis=1)
    state[:,0] = 0
    return state

# Return a matrix where each entry corresponds to the number of neighbours for
# corresponding entry in `state`
# Shift matrix and sum idea from: 
# https://www.r-bloggers.com/fast-conways-game-of-life-in-r/
def countNeighbours(state):
    N = north(state)
    S = south(state)
    W = west(state)
    E = east(state)

    NE = north(E)
    SE = south(E)
    NW = north(W)
    SW = south(W)

    directions = [N, S, E, W, NE, SE, NW, SW]

    return sum(directions)

def main():

    # Set up a toy state and see the results of counting neighbours
    state = np.zeros((5,5), uint8)
    state[2,2] = 1
    state[3,3] = 1
    state[3,2] = 1

    print(state)
    print(countNeighbours(state))


    return

main()

