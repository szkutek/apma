import numpy as np
import matplotlib.pyplot as plt
import imageio


def init_pos(bnum, N):
    boids_pos = [0] * bnum
    boids_vel = [0] * bnum
    for n in range(bnum):
        boids_pos[n] = np.array([np.random.rand() * N, np.random.rand() * N])
        boids_vel[n] = np.array([2., 1.])
    return boids_pos, boids_vel


def rule1(bj, boids_pos):
    """Rule 1: Boids try to fly towards the centre of mass of neighbouring boids. """
    pc = sum(boids_pos)
    pc -= bj
    pc = pc / (len(boids_pos) - 1)
    return (pc - bj) / 100


def distance(b1, b2):
    d = (b1[0] - b2[0]) ** 2 + (b1[1] - b2[1]) ** 2
    return np.sqrt(d)


def rule2(bj, boids_pos):
    """ Rule 2: Boids try to keep a small distance away from other objects (including other boids). """
    c = np.array([0., 0.])
    for pos in boids_pos:
        if distance(pos, bj) < 2:
            c -= pos - bj
    return c


def rule3(bv, boids_vel):
    """ Rule 3: Boids try to match velocity with near boids. """
    pv = sum(boids_vel)  # perceived velocity
    pv -= bv
    pv /= (len(boids_vel) - 1)
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


def move_boids(boids_pos, boids_vel, bnum, N):
    new_boids_pos = boids_pos.copy()
    new_boids_vel = boids_vel.copy()
    for i in range(bnum):
        v1 = rule1(boids_pos[i], boids_pos)
        v2 = rule2(boids_pos[i], boids_pos)
        v3 = rule3(boids_vel[i], boids_vel)
        v4 = bound_position(boids_pos[i], N)
        new_vel = boids_vel[i] + v1 + v2 + v3 + v4
        new_pos = boids_pos[i] + new_vel

        new_boids_pos[i] = new_pos
        new_boids_vel[i] = new_vel

    return new_boids_pos, new_boids_vel


def draw_boids(boids_pos, index):
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    x, y = list(zip(*boids_pos))
    plt.plot(x, y, '.')

    s = 'b' + "_" + str(index) + '.png'
    plt.savefig(s)
    plt.clf()


def movie(n, pathname, moviename, duration=0.3):
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
    for i in range(M):
        draw_boids(boids_pos, i)
        boids_pos, boids_vel = move_boids(boids_pos, boids_vel, bnum, grid_size)

    movie(M, 'b', 'boids1')
