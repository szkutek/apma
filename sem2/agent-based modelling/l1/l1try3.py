import numpy as np
import random as rnd


# automaton ~ fire spreads like an epidemic

# 't' tree; '*' fire; '_' empty; '.' burned tree
# 1 tree; 2 fire; 0 empty


def make_forest(L=10, p=1.0):
    pom = np.zeros([L + 2, L + 2])
    for i in range(L):
        pom[i + 1][1:L + 1] = [1 if rnd.random() < p else 0 for _ in range(L)]
    return pom


def print_forest(forest, state=0):
    for i in range(1, forest.shape[0] - 1):
        print([{0: '_', 1: 'T', 2: '*'}[cell] for cell in forest[i][1:forest.shape[1] - 1]])
    print('number of trees on fire: ', state)


def start_fire(forest):
    L = forest.shape[0] - 2
    state = 0
    # forest[1][1:L + 1] = [2 if forest[1][i + 1] == 1 else 0 for i in range(L)]
    for i in range(L):
        if forest[1][i + 1] == 1:
            forest[1][i + 1] = 2
            state += 1
        else:
            forest[1][i + 1] = 0
    return forest, state


def automaton(forest, st0):
    L = forest.shape[0] - 2
    st1 = st0
    state_change = True
    # while st0 > 0 and state_change is True:
    while state_change is True:
        state_change = False
        for x, y in np.ndindex(forest.shape):
            if 0 < x < L + 1 and 0 < y < L + 1:  # forest, st1 = check_neighbors(forest, x, y)
                if forest[x][y] == 2:  # if burning
                    for i in [x - 1, x, x + 1]:  # check all neighbours
                        for j in [y - 1, y, y + 1]:
                            if forest[i][j] == 1:  # if tree
                                forest[i][j] = 2
                                st1 += 1
                                state_change = True
                                print_forest(forest, st1)
    return forest, st1


if __name__ == '__main__':
    forest = make_forest(5, 0.5)
    print('BEFORE THE FIRE')
    print_forest(forest)
    #
    forest, state = start_fire(forest)
    print('\nTHE FIRE STARTED')
    print_forest(forest, state)
    #
    forest, state = automaton(forest, state)
    print('\nAFTER THE FIRE')
    print_forest(forest, state)
