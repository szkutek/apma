from pprint import pprint

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np


def init_model(M, N):
    road = [-1] * M
    chosen_indices = np.random.choice(M, N, replace=False)
    for i in chosen_indices:
        road[i] = 0
    return np.array(road)


def distance(m, road):
    d = 1
    M = len(road)
    while road[(m + d) % M] < 0:
        d += 1
    return d


def traffic_model(M, rho, p, I=10):
    N = int(M * rho)
    iterations = [0] * I
    iterations[0] = init_model(M, N)

    for i in range(1, I):
        prev_road = iterations[i - 1]
        curr_road = np.array([-1] * M)

        for m in range(M):
            vel = prev_road[m]
            if vel > -1:  # it's a car
                d = distance(m, prev_road)
                if vel < 5:
                    vel += 1
                if d < vel:
                    vel = d
                if vel > 1:
                    if np.random.random() < p:
                        vel -= 1

                curr_road[(m + vel) % M] = vel  # move
        iterations[i] = curr_road
    # return iterations
    return iterations[-1]


def animate(index):
    global prev_road, p
    prev_road = list(prev_road[0])
    curr_road = [-1] * M

    for m in range(M):
        vel = prev_road[m]
        if vel > -1:  # it's a car
            d = distance(m, prev_road)
            if vel < 5:
                vel += 1
            if d < vel:
                vel = d
            if vel > 1:
                if np.random.random() < p:
                    vel -= 1

            curr_road[(m + vel) % M] = vel  # move

    curr_road = np.array(curr_road).reshape(1, M)
    mat.set_data(curr_road)
    prev_road = curr_road
    return mat, curr_road


def plot_avg_velocity():
    R = np.arange(0.1, 1.0, 0.1)
    P = [0., .1, .5, .7]
    Res = []
    for p in P:
        res = []
        for r in R:
            tmp = traffic_model(M, r, p, I)
            tmp2 = np.array([x for x in tmp if x > -1])

            res.append(np.average(tmp2))

        plt.scatter(R, res)
        plt.title('Average velocity as a function of the density for p=' + str(p))
        plt.xlabel('rho')
        plt.ylabel('avg(velocity)')
        plt.savefig('avg-velocity-p=' + str(p) + '.png')
        plt.clf()

        Res.append(res)

    for i, _ in enumerate(P):
        plt.scatter(R, Res[i])
    plt.legend(P)
    plt.title('Average velocity as a function of the density for different p')
    plt.xlabel('rho')
    plt.ylabel('avg(velocity)')
    plt.savefig('avg-velocity-p' + '.png')


if __name__ == '__main__':
    I = 1000
    M = 100
    p = 0.3
    rho = .1  # .1, .2, .6
    # iterations = traffic_model(M, rho, p, I)

    N = int(M * rho)
    prev_road = init_model(M, N).reshape(1, M)

    fig, ax = plt.subplots()
    mat = ax.matshow(prev_road)
    ani = animation.FuncAnimation(fig, animate, interval=300)
    plt.show()
