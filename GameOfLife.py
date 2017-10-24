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



def main():

    # Set up a toy state and see the results of rolling it
    state = np.ones((5,5), uint8)
    #state[2,2] = 1
    #state[3,3] = 1
    #state[3,2] = 1

    print(state)
    print(north(state))
    print(south(state))
    print(west(state))
    print(east(state))
    

    return

main()

