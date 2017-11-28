import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rnd
from matplotlib.colors import ListedColormap


def distribute_agents(M, N, Nb):
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


def count_neighbours(state, x, y, mb, mr):
    N, M = state.shape
    m = mb if state[x][y] == 1 else mr
    nbrs = [(i % N, j % M)
            for i in range(x - m, x + m + 1)
            for j in range(y - m, y + m + 1)
            if not (i == x and j == y)]
    blue = 0
    red = 0
    for i, j in nbrs:
        if state[i][j] == 1:
            blue += 1
        elif state[i][j] == 2:
            red += 1
    return blue, red


def move_agent(lattice, c1, c2):
    N, M = lattice.shape

    new_c1 = rnd.randint(N)
    new_c2 = rnd.randint(M)

    while lattice[new_c1][new_c2] != 0:
        new_c1 = rnd.randint(N)
        new_c2 = rnd.randint(M)

    lattice[new_c1][new_c2] = lattice[c1][c2]
    lattice[c1][c2] = 0
    return lattice, new_c1, new_c2


def schelling_algorithm(lattice, agents_coord, jb, mb, jr, mr):
    changed = True
    cycles = 0
    while changed:
        changed = False
        for c in range(len(agents_coord)):
            c1, c2 = agents_coord[c]
            blue_nb, red_nb = count_neighbours(lattice, c1, c2, mb, mr)
            all_nb = blue_nb + red_nb
            if all_nb == 0 or ((lattice[c1][c2] == 1 and blue_nb / all_nb <= jb)
                               or (lattice[c1][c2] == 2 and red_nb / all_nb <= jr)):
                lattice, new_c1, new_c2 = move_agent(lattice, c1, c2)  # moves agents on the lattice
                agents_coord[c] = [new_c1, new_c2]
                changed = True
        cycles += 1
    return lattice, cycles, agents_coord


def segr_index(grid, agent_coord, mb, mr):
    index = 0.
    # mb, mr = 1, 1
    for c1, c2 in agent_coord:
        blue_nb, red_nb = count_neighbours(grid, c1, c2, mb, mr)
        all_nb = blue_nb + red_nb
        if all_nb > 0:
            if grid[c1][c2] == 1:
                index += blue_nb / all_nb
            else:
                index += red_nb / all_nb
    return index / len(agent_coord)


def schelling(M, N, Nb, jb, mb, jr, mr):
    starting_grid, blue_coord, red_coord = distribute_agents(M=M, N=N, Nb=Nb)
    agents_coord = np.array(blue_coord + red_coord)
    final_grid, cycles, agents_coord = schelling_algorithm(starting_grid.copy(), agents_coord,
                                                           jb=jb, mb=mb, jr=jr, mr=mr)
    return starting_grid, final_grid, cycles, agents_coord


def schellings_number_of_iterations(M, N, Nb, jb, mb, jr, mr):
    starting_grid, final_grid, cycles, agents_coord = schelling(M, N, Nb, jb, mb, jr, mr)
    return cycles


def schellings_segregation_index(M, N, Nb, jb, mb, jr, mr):
    starting_grid, final_grid, cycles, agents_coord = schelling(M, N, Nb, jb, mb, jr, mr)
    return segr_index(final_grid, agents_coord, mb, mr)


def save_schelling_plot(lattice, title='schelling', filename='schelling'):
    cmap = ListedColormap(['w', 'b', 'r'])
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 10)
    plt.title(title)
    ax.matshow(lattice, cmap=cmap)
    plt.savefig(filename + '.png')
    plt.close()


if __name__ == '__main__':
    grid1, grid2, cycles, agents_coord = schelling(100, 500, 250)

    save_schelling_plot(grid1, 'Schelling - starting positions of agents', 'm100-n500-b250-start')
    save_schelling_plot(grid2, 'Schelling - final positions of agents', 'm100-n500-b250-end')
