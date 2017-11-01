"""
Agnieszka Szkutek, 208619
"""

import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import imageio
import pylab
import networkx as nx


def random_walk(N=10):
    x = [0]
    y = [0]
    step = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for i in range(N):
        dx, dy = step[rnd.randint(0, 3)]
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)

    return x, y


def pearson_random_walk(N=10):
    x = [0]
    y = [0]

    for i in range(N):
        angle = 2 * np.pi * rnd.random()
        dy = np.sin(angle)
        dx = np.cos(angle)
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)

    return x, y


def random_walk_on_graph(G, start, N=10, pathname='graph_walk'):
    visited = [start]
    fig = pylab.figure()
    pos = nx.spring_layout(G)
    size = 200

    nx.draw_networkx_nodes(G, pos, node_color='0.75', node_size=size, alpha=0.8)
    nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='k', node_size=size, alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    pylab.savefig(pathname + '0.png')
    pylab.clf()

    for i in range(N):
        neighbors = G.neighbors(visited[-1])
        visited.append(neighbors[rnd.randint(0, len(neighbors) - 1)])

        nx.draw_networkx_nodes(G, pos, node_color='0.75', node_size=size, alpha=0.8)
        nx.draw_networkx_nodes(G, pos, nodelist=visited, node_color='0.25', node_size=size, alpha=0.8)
        nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='b', node_size=size, alpha=0.8)
        nx.draw_networkx_nodes(G, pos, nodelist=visited[-1:], node_color='r', node_size=size, alpha=0.8)

        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

        s = pathname + str(i + 1) + '.png'
        pylab.savefig(s)
        pylab.clf()
    pylab.close(fig)


def hitting_times(g, start):
    nodes = g.nodes()
    k = start

    ht = dict.fromkeys(nodes)
    ht[start] = 0
    nodes.remove(k)

    t = 1
    while len(nodes) > 0 and t < 1000 * len(nodes):
        neighbors = g.neighbors(k)
        k = neighbors[rnd.randint(0, len(neighbors) - 1)]

        if k in nodes:
            ht[k] = t
            nodes.remove(k)
        t = t + 1

    return ht


def average_hitting_times(g, start, N=100):
    avg_ht = {key: 0 for key in g.nodes()}
    for i in range(N):
        ht = hitting_times(g, start)
        for key, val in avg_ht.items():
            avg_ht[key] = val + ht[key]

    for key, val in avg_ht.items():
        avg_ht[key] = val / N
    return avg_ht


def draw_plot(x, y):
    margin = 2
    # fig_size = 10
    # fig = pylab.figure(figsize=(fig_size, fig_size))
    fig = pylab.figure()
    p = fig.add_subplot(111)
    p.plot(x, y, marker='o', linestyle='-', color='black')
    p.plot(x[0], y[0], marker='o', color='blue')
    p.plot(x[-1], y[-1], marker='o', color='red')
    p.grid(True)
    pylab.tight_layout()

    p.set_xlim([min(x) - margin, max(x) + margin])
    p.set_ylim([min(y) - margin, max(y) + margin])
    plt.xlabel('x')
    plt.ylabel('y')

    pylab.show()
    # pylab.close(fig)


def save_plot(x, y, pathname):
    # path = list(zip(x, y))
    xmin, xmax, ymin, ymax = min(x), max(x), min(y), max(y)

    fig_size = 10
    fig = pylab.figure(figsize=(fig_size, fig_size))
    p = fig.add_subplot(111)

    margin = 2
    # # #
    for i in range(len(x)):
        p.plot(x[:i + 1], y[:i + 1], marker='o', linestyle='-', color='black')
        # p.plot(x[i - 1:i + 1], y[i - 1:i + 1], marker='o', linestyle='-', color='red')
        p.plot(x[i], y[i], marker='o', color='red')

        p.grid(True)
        # pylab.tight_layout()

        p.set_xlim([xmin - margin, xmax + margin])
        p.set_ylim([ymin - margin, ymax + margin])

        s = pathname + str(i) + '.png'
        pylab.savefig(s)
    pylab.clf()
    pylab.close(fig)


def movie(n, pathname, moviename, duration=0.2):
    frames = []
    for i in range(n):
        path = pathname + str(i + 1) + '.png'
        frames.append(imageio.imread(path))

    kargs = {'duration': duration}
    imageio.mimwrite(moviename + '.gif', frames, 'gif', **kargs)


def right_half_plane(x):
    return sum(i > 0 for i in x)


def first_quadrant(x, y):
    return sum(i > 0 and j > 0 for i, j in list(zip(x, y)))


def histogram(M=10, N=100):
    """
    :param M: number of simulations 
    :param N: number of steps in one simulation
    """
    An = []
    Bn = []
    for i in range(M):
        x, y = pearson_random_walk(N)
        # draw_plot(x, y)
        An.append(right_half_plane(x) / N)
        Bn.append(first_quadrant(x, y) / N)

    print('<A_N> = ' + str(np.average(An)))
    print('<B_N> = ' + str(np.average(Bn)))
    plot_hist(An, name='A_N')
    plot_hist(Bn, name='B_N')


def plot_hist(data, log=False, name=''):
    fig = plt.figure()
    plt.hist(data, normed=True, log=log)
    plt.title(name + ' histogram')
    plt.xlabel(name)
    plt.ylabel('frequency')
    plt.show()
    # plt.close(fig)


if __name__ == "__main__":
    # # # # 1
    n1 = 50
    x, y = random_walk(n1)
    # draw_plot(x, y)
    save_plot(x, y, pathname='fig')
    movie(n1, 'fig', 'fig1', duration=0.2)

    # # # # 2
    n = 1000
    histogram(M=100, N=n)  # M - number of walks, N - number of steps
    for i in range(3):
        x, y = pearson_random_walk(n)
        draw_plot(x, y)

    # # # # 3a
    number_of_nodes = 20
    n = 20

    g1 = nx.barabasi_albert_graph(number_of_nodes, 2)
    random_walk_on_graph(g1, g1.nodes()[0], n, pathname='graph_walk1')
    movie(n, 'graph_walk1', 'rw_ba', duration=0.5)
    g2 = nx.watts_strogatz_graph(number_of_nodes, 4, 0.5)
    random_walk_on_graph(g2, g2.nodes()[0], n, pathname='graph_walk2')
    movie(n, 'graph_walk2', 'rw_ws', duration=0.5)

    # # # # 3b
    ht1 = average_hitting_times(g1, g1.nodes()[0], 100)
    print('Average hitting times for a Barabassi-Albert graph')
    print(ht1)
    ht2 = average_hitting_times(g2, g2.nodes()[0], 100)
    print('Average hitting times for a Watts-Strogatz graph')
    print(ht2)
