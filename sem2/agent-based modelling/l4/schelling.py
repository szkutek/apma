import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
from matplotlib import animation


def distribute_agents(N, Nb) -> (np.array, np.array, np.array):
    M = 3
    Nr = N - Nb

    arr = np.zeros([M, M], int)
    indices = list(np.ndindex(arr.shape))

    choice = rnd.choice(len(indices), Nb, replace=False)  # from index of indices
    blue_coord = [indices[b] for b in choice]  # the chosen indices
    for b1, b2 in blue_coord:
        arr[b1][b2] = 1

    leftover_coord = [(i0, i1) for i0, i1 in indices if arr[i0][i1] != 1]

    choice = rnd.choice(len(leftover_coord), Nr, replace=False)
    red_coord = [indices[r] for r in choice]
    for r1, r2 in red_coord:
        arr[r1][r2] = 2

    # return arr, np.array(blue_coord), np.array(red_coord)
    return arr, blue_coord, red_coord


def count_neighbours(state, x, y, m):
    N, M = state.shape
    nbrs = [(i, j)
            for i in range(x - m, x + m + 1)
            for j in range(y - m, y + m + 1)
            if not (i == x and j == y) and 0 <= i < N and 0 <= j < M]
    blue = 0
    red = 0
    empty = 0
    for i, j in nbrs:
        if state[i][j] == 1:
            blue += 1
        elif state[i][j] == 2:
            red += 1
        else:
            empty += 1

    return blue, red, empty


# def schelling(lattice, blue_coord, red_coord, jt, mt=1):
def schelling(frame):
    agents_coord = blue_coord + red_coord
    required_num = jt * mt
    for c1, c2 in agents_coord:
        blue_nb, red_nb, empty_nb = count_neighbours(lattice, c1, c2, mt)
        all_nb = blue_nb + red_nb + empty_nb
        if lattice[c1][c2] == 1:
            if blue_nb / all_nb < jt:
                # move the individual to a randomly selected new empty location ????????????????????????
                pass
        elif lattice[c1][c2] == 2:
            if red_nb / all_nb < jt:
                # move the individual to a randomly selected new empty location ????????????????????????
                pass


if __name__ == '__main__':
    # print(distribute_agents(4, 3))
    lattice, blue_coord, red_coord = distribute_agents(4, 3)
    jt, mt = .5, 1

    fig, ax = plt.subplots()
    plt.title('the animation')
    mat = ax.matshow(lattice)
    ani = animation.FuncAnimation(fig, schelling, interval=500)
    plt.show()
