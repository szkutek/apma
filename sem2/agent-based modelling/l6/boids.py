import numpy as np
import matplotlib.pyplot as plt
import imageio


def init_pos(bnum, N):
    boids_pos = [np.array([np.random.rand() * N, np.random.rand() * N]) for _ in range(bnum)]
    boids_vel = [np.array([1, 2]) for _ in range(bnum)]
    return boids_pos, boids_vel


def rule1(bj, boids_pos):
    """Rule 1: Boids try to fly towards the centre of mass of neighbouring boids. """
    tmp = [pos for pos in boids_pos if distance(bj, pos) < 20]
    n = len(tmp) - 1
    pc = (sum(tmp) - bj) / n if n > 0 else bj

    return (pc - bj) / 100


def distance(b1, b2):
    d = (b1[0] - b2[0]) ** 2 + (b1[1] - b2[1]) ** 2
    return np.sqrt(d)


def rule2(bj, boids_pos, obstacles):
    """ Rule 2: Boids try to keep a small distance away from other objects (including other boids). """

    c = np.array([0., 0.])
    for pos in boids_pos:
        if distance(pos, bj) < 5:
            c -= (pos - bj) / 2
    for obj in obstacles:
        if distance(obj, bj) < 5:
            c -= (obj - bj)
    return c


def rule3(bj, bv, boids_pos, boids_vel):
    """ Rule 3: Boids try to match velocity with neighbouring boids. """
    pv = np.array([0., 0.])  # perceived velocity
    n = 0
    for pos, vel in zip(boids_pos, boids_vel):
        if distance(bj, pos) < 20:
            pv += vel
            n += 1
    pv -= bv
    n -= 1
    pv = pv / n if n > 0 else pv
    return (pv - bv) / 8


def bound_position(bj, N):
    xmin, xmax, ymin, ymax = 10, N - 10, 10, N - 10
    vx, vy = 0., 0.
    x, y = bj

    if x < xmin:
        vx = 1
    elif x > xmax:
        vx = -1

    if y < ymin:
        vy = 1
    elif y > ymax:
        vy = -1

    return np.array([vx, vy])


def move_boids(boids_pos, boids_vel, bnum, N, obstacles):
    new_boids_pos = boids_pos.copy()
    new_boids_vel = boids_vel.copy()
    for i in range(bnum):
        v1 = rule1(boids_pos[i], boids_pos)
        v2 = rule2(boids_pos[i], boids_pos, obstacles)
        v3 = rule3(boids_pos[i], boids_vel[i], boids_pos, boids_vel)
        v4 = bound_position(boids_pos[i], N)
        new_vel = boids_vel[i] + v1 + v2 + v3 + v4
        new_pos = boids_pos[i] + new_vel

        new_boids_pos[i] = new_pos
        new_boids_vel[i] = new_vel

    return new_boids_pos, new_boids_vel


def draw_boids(boids_pos, index, obstacles):
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    x, y = list(zip(*obstacles))
    plt.plot(x, y, '.r')

    x, y = list(zip(*boids_pos))
    plt.plot(x, y, '.')

    s = 'b' + "_" + str(index) + '.png'
    plt.savefig(s)
    plt.clf()


def movie(n, pathname, moviename, duration=0.2):
    frames = []
    for i in range(n):
        path = pathname + "_" + str(i) + '.png'
        frames.append(imageio.imread(path))

    kargs = {'duration': duration}
    imageio.mimwrite(moviename + '.gif', frames, 'gif', **kargs)


if __name__ == '__main__':
    grid_size = 100
    bnum = 10

    boids_pos, boids_vel = init_pos(bnum, grid_size)
    plt.figure()

    M = 100
    obstacles = [np.array([np.random.rand() * grid_size, np.random.rand() * grid_size]) for _ in range(5)]

    for i in range(M):
        draw_boids(boids_pos, i, obstacles)
        boids_pos, boids_vel = move_boids(boids_pos, boids_vel, bnum, grid_size, obstacles)

    movie(M, 'b', 'boids1')
