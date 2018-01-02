import numpy as np
import matplotlib.pyplot as plt
import imageio


class Boid:
    def __init__(self, n, x, y, vx, vy):
        self.n = n
        self.pos = np.array([x, y])
        self.vel = np.array([vx, vy])


def init_pos(bnum, N):
    boids = [0] * bnum
    for n in range(bnum):
        boids[n] = Boid(n, np.random.randint(0, N), np.random.randint(0, N), 0., 0.)
    return boids


def rule1(boid, boids):
    """Rule 1: Boids try to fly towards the centre of mass of neighbouring boids. """
    pc = np.array([0., 0.])
    for b in boids:
        pc += b.pos
    pc -= boid.pos
    pc = pc / (len(boids) - 1)
    return (pc - boid.pos) / 100


def distance(b1, b2):
    d = (b1[0] - b2[0]) ** 2 + (b1[1] - b2[1]) ** 2
    return np.sqrt(d)


def rule2(boid, boids):
    """ Rule 2: Boids try to keep a small distance away from other objects (including other boids). """
    c = np.array([0., 0.])
    for b in boids:
        if distance(b.pos, boid.pos) < 1:
            c -= b.pos - boid.pos
    return c


def rule3(boid, boids):
    """ Rule 3: Boids try to match velocity with near boids. """
    pv = np.array([0., 0.])
    for b in boids:
        pv += b.vel
    pv -= boid.vel
    pv /= (len(boids) - 1)
    return (pv - boid.vel) / 8


def move_boids(boids, N):
    new_boids = [0] * len(boids)
    for i in range(len(boids)):
        b = boids[i]

        v1 = rule1(b, boids)
        v2 = rule2(b, boids)
        v3 = rule3(b, boids)
        new_vel = b.vel + v1 + v2 + v3
        new_pos = b.pos + b.vel

        new_boids[i] = Boid(i, new_pos[0], new_pos[1], new_vel[0], new_vel[1])

    return new_boids


def draw_boids(boids, index):
    plt.xlim(0, N)
    plt.ylim(0, N)
    for b in boids:
        plt.plot(b.pos[0], b.pos[1], '.')

    s = 'b' + "_" + str(i) + '.png'
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
    N = 10
    bnum = 10

    boids = init_pos(bnum, N)
    plt.figure()

    M = 100
    for i in range(M):
        draw_boids(boids, i)
        boids = move_boids(boids, N)

    movie(M, 'b', 'boids1')
