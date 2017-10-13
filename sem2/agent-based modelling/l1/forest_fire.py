import numpy as np
import random as rnd


# 'T' tree; 'X' fire; ' ' empty; '_' burned tree
# 1 tree; 2 fire; 0 empty; 3 burned tree

def forest_fire(p, L, direction='0', strength=1):
    return automaton(start_fire(make_forest(L, p)), direction, strength)


def make_forest(L=10, p=1.0):
    pom = np.zeros([L, L])
    for i in range(L):
        pom[i] = [1 if rnd.random() < p else 0 for _ in range(L)]
    return pom


def print_forest(forest):
    for i in range(forest.shape[0]):
        print([{0: ' ', 1: 'T', 2: 'X', 3: '_'}[cell] for cell in forest[i]])
    print('')


def start_fire(forest):
    L = forest.shape[0]
    for i in range(L):
        if forest[0][i] == 1:
            forest[0][i] = 2
        else:
            forest[0][i] = 0
    return forest


def wind_direction(x, y, direction, strength=1):
    i = strength
    Dir = {
        '0': [(x - i, y - i), (x - i, y), (x - i, y + i),
              (x, y - i), (x, y + i),
              (x + i, y - i), (x + i, y), (x + i, y + i)],
        # 'N': [(x - i, y)],
        # 'S': [(x + i, y)],
        # 'W': [(x, y - i)],
        # 'E': [(x, y + i)]
        'N': [(x - i, y - i), (x - i, y), (x - i, y + i)],
        'S': [(x + i, y - i), (x + i, y), (x + i, y + i)],
        'W': [(x - i, y - i), (x, y - i), (x + i, y - i)],
        'E': [(x - i, y + i), (x, y + i), (x + i, y + i)]
    }
    return Dir[direction]


def automaton(f1=np.array([]), direction='0', strength=1):
    L = f1.shape[0]
    state_change = True
    f2 = f1.copy()  # forest before and after the move

    while state_change is True:
        state_change = False

        for x, y in np.ndindex(f1.shape):
            str0 = strength

            if f1[x][y] == 1:  # is tree
                while str0 > 0:
                    wind = wind_direction(x, y, direction, strength=str0)
                    for i, j in wind:
                        if 0 <= i < L and 0 <= j < L:  # if neighbour in grid
                            if f1[i][j] == 2:  # if the neighbour is burning
                                f2[x][y] = 2
                                state_change = True
                    str0 -= 1

            elif f1[x][y] == 2:
                f2[x][y] = 3
                state_change = True

        # print_forest(f1)  # TODO remove print
        f1 = f2.copy()

    return f2


if __name__ == '__main__':
    forest_fire(0.5, 5, 'W', 2)
