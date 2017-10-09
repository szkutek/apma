import numpy as np
import random as rnd


# 't' tree; '*' fire; '_' empty; '.' burned tree
# 1 tree; 2 fire; 0 empty; 3 burned tree
# TODO is state necessary?

def forest_fire(p, L):
    f, s = (start_fire(make_forest(L, p)))
    return automaton(f, s)


def make_forest(L=10, p=1.0):
    pom = np.zeros([L, L])
    for i in range(L):
        pom[i] = [1 if rnd.random() < p else 0 for _ in range(L)]
    return pom


def print_forest(forest, state=0):
    for i in range(forest.shape[0]):
        print([{0: '_', 1: 'T', 2: 'X', 3: 'v'}[cell] for cell in forest[i]])


def start_fire(forest):
    L = forest.shape[0]
    state = 0
    # forest[1][1:L + 1] = [2 if forest[1][i + 1] == 1 else 0 for i in range(L)]
    for i in range(L):
        if forest[0][i] == 1:
            forest[0][i] = 2
            state += 1
        else:
            forest[0][i] = 0
    return forest, state


def automaton(f1=np.array([]), st0=0):
    L = f1.shape[0]
    st1 = st0
    state_change = True
    f2 = f1.copy()  # forest before and after the move
    
    while state_change is True:
        state_change = False

        for x, y in np.ndindex(f1.shape):
            if f1[x][y] == 1:  # is tree
                for i, j in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                             (x, y - 1), (x, y + 1),
                             (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]:
                    if 0 <= i < L and 0 <= j < L:  # if in grid
                        if f1[i][j] == 2:  # if burning
                            f2[x][y] = 2
                            st1 += 1
                            state_change = True
            elif f1[x][y] == 2:
                f2[x][y] = 3
                st1 -= 1
                state_change = True
        # print_forest(f1, st1)
        f1 = f2.copy()

    return f2


if __name__ == '__main__':
    forest = make_forest(5, 0.5)
    print('BEFORE THE FIRE')
    print_forest(forest)
    #
    forest, state = start_fire(forest)
    print('\nTHE FIRE STARTED')
    print_forest(forest, state)
    #
    forest = automaton(forest, state)
    print('\nAFTER THE FIRE')
    print_forest(forest)
