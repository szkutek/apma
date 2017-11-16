import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
from matplotlib import animation


def distribute_agents(N, Nb) -> (np.array, np.array, np.array):
    M = 4
    Nr = N - Nb

    arr = np.zeros([M, M], int)
    indices = list(np.ndindex(arr.shape))

    choice = rnd.choice(len(indices), Nb, replace=False)  # from index of indices
    blue_coord = [indices[b] for b in choice]  # the chosen indices
    for b1, b2 in blue_coord:
        arr[b1][b2] = 1

    leftover_coord = [(i0, i1) for i0, i1 in indices if arr[i0][i1] != 1]

    choice = rnd.choice(len(leftover_coord), Nr, replace=False)
    red_coord = [leftover_coord[r] for r in choice]
    for r1, r2 in red_coord:
        arr[r1][r2] = 2

    # return arr, np.array(blue_coord), np.array(red_coord)
    return arr, blue_coord, red_coord


def count_neighbours(state, x, y, m):
    N, M = state.shape
    nbrs = [(i % N, j % M)
            for i in range(x - m, x + m + 1)
            for j in range(y - m, y + m + 1)
            if not (i == x and j == y)]
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


# def schelling(lattice, blue_coord, red_coord, jb, mb=1):
def schelling(frame):
    global agents_coord

    for c in range(len(agents_coord)):
        c1, c2 = agents_coord[c]
        blue_nb, red_nb, empty_nb = count_neighbours(lattice, c1, c2, mb)
        all_nb = blue_nb + red_nb
        if all_nb > 0:
            if (lattice[c1][c2] == 1 and blue_nb / all_nb <= jb) or \
                    (lattice[c1][c2] == 2 and red_nb / all_nb <= jr):
                new_c1, new_c2 = move_agent(c1, c2)
                agents_coord[c] = [new_c1, new_c2]

    mat.set_data(lattice)
    return mat, lattice


def move_agent(c1, c2):
    N, M = lattice.shape

    new_c1 = rnd.randint(N)
    new_c2 = rnd.randint(M)

    while lattice[new_c1][new_c2] != 0:
        new_c1 = rnd.randint(N)
        new_c2 = rnd.randint(M)

    lattice[new_c1][new_c2] = lattice[c1][c2]
    lattice[c1][c2] = 0
    return new_c1, new_c2


if __name__ == '__main__':
    lattice, blue_coord, red_coord = distribute_agents(4, 2)
    agents_coord = np.array(blue_coord + red_coord)
    jb, mb = .5, 1
    jr, mr = .5, 1

    fig, ax = plt.subplots()
    plt.title('the animation')
    mat = ax.matshow(lattice)
    ani = animation.FuncAnimation(fig, schelling, interval=500)
    plt.show()
