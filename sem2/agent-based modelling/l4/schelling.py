import numpy as np
import numpy.random as rnd


def distribute_agents(N, Nb):
    # Nr = N - Nb
    M = 10
    MM = M * M
    Nr = N - Nb
    # arr = np.ndarray([M, M])
    # arr_ind = np.ndindex(arr)
    # # choose blue and red agents
    # blue_coord = rnd.choice(arr_ind, Nb, replace=False)
    # red_coord = rnd.choice(arr_ind, Nr, replace=False)
    arr = np.empty(MM)
    arr.fill(int(0))
    blue_coord = rnd.choice(MM, Nb, replace=False)  # from list 0:MM-1

    leftover_coord = [*set(range(MM)) - set(blue_coord)]
    red_coord = rnd.choice(leftover_coord, Nr, replace=False)

    for b in blue_coord:
        arr[b] = 1
    for r in red_coord:
        arr[r] = 2

    return arr.reshape(M, M)


print(distribute_agents(5, 4))
