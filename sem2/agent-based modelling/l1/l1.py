import numpy as np
import random as rnd


def make_forest(L=10, p=1.0):
    forest = np.array([
        ['t' if rnd.random() < p else '.' for _ in range(L)] for _ in range(L)])
    # for x, y in np.ndindex(forest.shape):
    #     forest[x][y] = 't' if rnd.random() < p else '.'
    return forest


def print_forest(forest):
    for row in forest:
        print(row)


def start_fire(forest):
    # for i in range(len(forest[0])):
    #     if forest[0][i] == 't':
    #         forest[0][i] = '*'
    forest[0] = ['*' if forest[0][i] == 't' else '.' for i in range(len(forest))]
    return forest


def automaton(forest):
    for j, k in np.ndindex(forest.shape):
        if forest[j][k] == '*':
            forest[j][k + 1] = '*'
        forest[j][k] = '.'

    return forest


def check_neighbors(forest, x, y):
    for i in [x - 1, x, x + 1]:
        for j in [y - 1, y, y + 1]:
            if (0 < i < forest.shape[0]) and (0 < j < forest.shape[1]):
                if forest[i][j] == 't':
                    forest[i][j] = '*'
                    print(forest)
                    check_neighbors(forest, i, j)
    forest[x][y] = '.'
    return forest


print('BEFORE THE FIRE')
forest = make_forest(5, 0.7)
print_forest(forest)

print('\nTHE FIRE STARTED')
forest = start_fire(forest)
print_forest(forest)

print('\nAFTER THE FIRE')
forest = automaton(forest)
print_forest(forest)
