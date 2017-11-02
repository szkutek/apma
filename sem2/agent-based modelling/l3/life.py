from random import random

import numpy as np
import matplotlib.pyplot as plt
import imageio


# TODO change implementation?, change animation (don't save, the process could be infinite),
# TODO maybe use matshow http://electronut.in/a-simple-python-matplotlib-implementation-of-conways-game-of-life/

def create_random_grid(N, M, p):
    return np.array([[1 if random() < p else 0 for _ in range(M)] for _ in range(N)])


def neighbours(state, x, y):
    N, M = state.shape
    nbrs = [(i, j)
            for i in [x - 1, x, x + 1]
            for j in [y - 1, y, y + 1]
            if not (i == x and j == y) and 0 <= i < N and 0 <= j < M]
    alive = 0
    for i, j in nbrs:
        alive += state[i][j]
    return alive


def game_of_life(initial_state, filename):
    next_state = initial_state.copy()
    N, M = initial_state.shape
    state_change = True
    plot_i = 0
    while state_change:
        state_change = False
        for x, y in np.ndindex(initial_state.shape):
            live_neighbours = neighbours(initial_state, x, y)

            if initial_state[x][y] == 1:
                if live_neighbours < 2 or live_neighbours > 3:
                    next_state[x, y] = 0  # underpopulation or overpopulation
                    state_change = True
            else:
                if live_neighbours == 3:
                    next_state[x][y] = 1
                    state_change = True

        success = save_plot(plot_i, initial_state, filename)
        if success:
            plot_i += 1

        initial_state = next_state.copy()
    return plot_i


def save_plot(i, game_state, pathname):
    N, M = game_state.shape
    points = [(i, j) for i, j in np.ndindex(game_state.shape) if game_state[i][j]]
    if len(points):
        x, y = zip(*points)
    else:
        return 1
    xmin, xmax, ymin, ymax = 0, M, 0, N

    fig_size = 10
    fig = plt.figure(figsize=(fig_size, fig_size))
    p = fig.add_subplot(111)

    margin = 0
    p.plot(x, y, linestyle='None', marker='o', color='k')
    p.grid(True)
    p.set_xlim([xmin - margin, xmax + margin])
    p.set_ylim([ymin - margin, ymax + margin])

    s = pathname + "_" + str(i) + '.png'
    plt.savefig(s)
    # plt.clf()
    plt.close(fig)
    return 0


def movie(n, filename, moviename, duration=0.2):
    frames = []
    for i in range(n):
        path = filename + "_" + str(i) + '.png'
        frames.append(imageio.imread(path))

    kargs = {'duration': duration}
    imageio.mimwrite(moviename + '.gif', frames, 'gif', **kargs)


if __name__ == '__main__':
    grid = create_random_grid(5, 5, 0.5)

    n = game_of_life(grid, 'test')
    movie(n, 'test', 'test_movie', 0.5)
