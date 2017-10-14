import random as rnd
import numpy as np


# 'T' tree; 'X' fire; ' ' empty; '_' burned tree
# 1 tree; 2 fire; 0 empty; 3 burned tree

def forest_fire(p, L, Dir='0', Str=1):
    return automaton(start_fire(make_forest(L, p)), Dir, Str)


def make_forest(L=10, p=1.0):
    pom = np.zeros([L, L])
    for i in range(L):
        pom[i] = [1 if rnd.random() < p else 0 for _ in range(L)]
    return pom


def print_forest(forest):
    for i in range(forest.shape[0]):
        print([{0: ' ', 1: 'T', 2: 'X', 3: '_'}[cell] for cell in forest[i]])
    print('')


def start_fire(forest=np.array([])):
    forest[0] = [2 if cell == 1 else 0 for cell in forest[0]]
    return forest


def wind_direction(x, y, Dir, Str=1):
    i = Str
    Directions = {
        '0': [(x - i, y - i), (x - i, y), (x - i, y + i),
              (x, y - i), (x, y + i),
              (x + i, y - i), (x + i, y), (x + i, y + i)],
        'N': [(x - i, y - i), (x - i, y), (x - i, y + i)],
        'S': [(x + i, y - i), (x + i, y), (x + i, y + i)],
        'W': [(x - i, y - i), (x, y - i), (x + i, y - i)],
        'E': [(x - i, y + i), (x, y + i), (x + i, y + i)]
    }
    return Directions[Dir]  # if Str > 0 else []


def direction(x, y, Dir, Str=1):
    if Dir == '0':
        res = [(x + i, y + j) for i in range(-Str, Str + 1) for j in range(-Str, Str + 1)]

    elif Dir == 'N':
        res = [(x - s, y + i) for s in range(1, Str + 1) for i in range(-s, s + 1)]
    elif Dir == 'S':
        res = [(x + s, y + i) for s in range(1, Str + 1) for i in range(-s, s + 1)]
    elif Dir == 'W':
        res = [(x + i, y - s) for s in range(1, Str + 1) for i in range(-s, s + 1)]
    elif Dir == 'E':
        res = [(x + i, y + s) for s in range(1, Str + 1) for i in range(-s, s + 1)]
    else:
        res = []
    return res


def automaton(f1=np.array([]), Dir='0', Str=1):
    L = f1.shape[0]
    state_change = True
    f2 = f1.copy()  # forest before and after the move

    while state_change:
        state_change = False

        for x, y in np.ndindex(f1.shape):

            if f1[x][y] == 1:  # is tree
                str0 = Str
                caught_fire = False

                while not caught_fire and str0 > 0:  # check neighbours until f[x,y] catches fire or all are checked
                    wind = direction(x, y, Dir, Str=str0)
                    for i, j in wind:
                        if 0 <= i < L and 0 <= j < L:  # if neighbour is in grid
                            if f1[i][j] == 2:  # if the neighbour is burning
                                f2[x][y] = 2
                                state_change = True
                                caught_fire = True
                                break
                    str0 -= 1

            elif f1[x][y] == 2:
                f2[x][y] = 3
                state_change = True

        # print_forest(f1)  # TODO remove print
        f1 = f2.copy()

    return f2


if __name__ == '__main__':
    forest_fire(0.5, 50, 'W', 2)

    # f = np.array([[0, 2, 2, 0, 0],
    #               [1, 1, 0, 0, 1],
    #               [0, 0, 0, 0, 0],
    #               [1, 1, 1, 1, 0],
    #               [1, 0, 1, 0, 0]])
    # automaton(f, 'W', 2)
