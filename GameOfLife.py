import numpy as np
from numpy import uint8
import pygame
from pygame import surfarray
from pygame.locals import *
import sys

RESOLUTION = (50,50)
SCALE = 10
DELAY = 300

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

# Returns the mask of which cells have exactly 2 or 3 neighbours
livingCellsMask = np.vectorize(lambda x : x==2 or x==3)

# Returns the mask of which cells have exactly 3 neighbours
deadCellsMask = np.vectorize(lambda x : x==3)

# Generate the next state in the game according to the rules:
# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
# 1. A living cell with 2 or 3 neighbours lives on
# 2. A dead cell with exactly 3 neighbours spawns
def nextState(state):

    neighbourCounts = countNeighbours(state)

    toStayAlive = state * livingCellsMask(neighbourCounts)

    toSpawn = (1-state) * deadCellsMask(neighbourCounts)

    state = toStayAlive + toSpawn

    return state

# Draw the given state, scaled by SCALE
def graphics(state):
    state = np.transpose(state)
    largeState = np.kron(state*255, np.ones((SCALE,SCALE)))
    screen = pygame.display.set_mode(largeState.shape[:2], 0, 8)
    surfarray.blit_array(screen, largeState)
    pygame.display.update()
    return

# Animate all subsequent states from given state with delay
def animateLife(state):

    timeDelay = DELAY

    graphics(state)

    while 1:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                raise SystemExit()
            elif e.type == pygame.KEYDOWN:
                if e.key == ord('f'): # faster
                    timeDelay -= 10
                elif e.key == ord('s'): # slower
                    timeDelay += 10


        state = nextState(state)
        graphics(state)
        pygame.time.delay(timeDelay)


# Display a blank board.  User clicks fill the position with a live cell.
# Return the board after a key is pressed.
def getBoard(state):

    graphics(state)

    gettingInput = True
    while gettingInput:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.exit()
                raise SystemExit()
            elif e.type == pygame.KEYDOWN:
                gettingInput = False
            elif e.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x = pos[0]//SCALE
                y = pos[1]//SCALE
                state[x,y] = 1
                graphics(np.transpose(state))

    return np.transpose(state)


def main():
    global RESOLUTION
    pygame.init()

    print("\n".join(sys.argv))

    if len(sys.argv) > 1:
        if sys.argv[1] == "random":
            state = np.random.choice([0, 1], size=RESOLUTION)
        else:
            state = np.loadtxt(sys.argv[1], dtype = uint8)
            RESOLUTION = state.shape[:2]
    else:
        state = getBoard(np.zeros(RESOLUTION, dtype = uint8))

    animateLife(state)




    return

main()

