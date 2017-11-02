import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# TODO read input from text file


def create_random_grid(N, M, p):
    # return np.array([[1 if random() < p else 0 for _ in range(M)] for _ in range(N)])
    return np.array([1 if np.random.random() < p else 0 for _ in range(M * N)]).reshape(N, M)


def count_neighbours(state, x, y):
    N, M = state.shape
    nbrs = [(i, j)
            for i in [x - 1, x, x + 1]
            for j in [y - 1, y, y + 1]
            if not (i == x and j == y) and 0 <= i < N and 0 <= j < M]
    alive = 0
    for i, j in nbrs:
        alive += state[i][j]
    return alive


def next_generation(frame):
    global init_state
    next_state = init_state.copy()
    for x, y in np.ndindex(init_state.shape):
        live_neighbours = count_neighbours(init_state, x, y)

        if init_state[x][y] == 1:
            if live_neighbours < 2 or live_neighbours > 3:
                next_state[x, y] = 0  # underpopulation or overpopulation
        else:
            if live_neighbours == 3:
                next_state[x][y] = 1

    mat.set_data(next_state)
    init_state = next_state
    return mat, next_state


def init_from_file(filename):
    file = open(filename, 'r')
    res = [[int(char) for char in line if char == '1' or char == '0'] for line in file.readlines()]
    file.close()
    return np.array(res)


def examples():
    # init_state = init_from_file('glider.txt')
    # init_state = init_from_file('small_exploder.txt')
    # init_state = init_from_file('exploder.txt')
    # init_state = init_from_file('10_cell_row.txt')
    # init_state = init_from_file('small_spaceship.txt')
    init_state = init_from_file('tumbler.txt')

    fig, ax = plt.subplots()
    ax.matshow(init_state)
    plt.title('initial state')
    return init_state


if __name__ == '__main__':
    # init_state = create_random_grid(100, 100, 0.1)
    init_state = examples()

    fig, ax = plt.subplots()
    plt.title('the animation')
    mat = ax.matshow(init_state)
    ani = animation.FuncAnimation(fig, next_generation, interval=200)
    plt.show()
