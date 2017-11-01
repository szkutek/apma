"""
Agnieszka Szkutek, 208619
"""

import random as rnd
import bisect
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pickle
import numpy
import powerlaw

numpy.seterr(divide='ignore', invalid='ignore')


def choices(population, *, weights=None, k=1):
    """Return a k sized list of population elements chosen with replacement."""
    if weights is None:
        total = len(population)
        return [population[int(rnd.random() * total)] for i in range(k)]

    if len(weights) != len(population):
        raise ValueError('The number of weights does not match the population')
    cum_weights = list(itertools.accumulate(weights))
    total = cum_weights[-1]
    return [population[bisect.bisect(cum_weights, rnd.random() * total)] for i in range(k)]


def random_graph(N=0, P=1.0):
    G = nx.Graph()
    nodes = [i for i in range(N)]
    G.add_nodes_from(nodes)
    for i in range(N):
        for j in range(i + 1, N):
            if rnd.random() < P:
                G.add_edge(nodes[i], nodes[j])
    return G


def watts_strogatz_graph(N=0, K=2, B=1.0):
    K = K if (K % 2) == 0 else K - 1  # number of neighbours
    G = nx.Graph()
    nodes = [i for i in range(N)]
    G.add_nodes_from(nodes)
    # starting connections
    for i in range(N):
        for k in range(K // 2):
            j = (i + 1 + k) % N
            G.add_edge(nodes[i], nodes[j])

    # rewire connections
    for i in range(N):
        # print(G.edges())
        for j in range(N):
            if i != j and G.has_edge(nodes[i], nodes[j]):
                if rnd.random() < B:
                    k = rnd.randint(0, N - 1)  # mozna rnd.choice() z mozliwych do wyboru wierzcholkow
                    while i == k or G.has_edge(nodes[i], nodes[k]):
                        k = rnd.randint(0, N - 1)
                    possible_nodes = [k for k in G.nodes() if k not in G.neighbors(i) + [i]]
                    k = rnd.choice(possible_nodes)
                    G.add_edge(nodes[i], nodes[k])
                    G.remove_edge(nodes[i], nodes[j])
                    # print('Zamiana (' + str(i) + ',' + str(j) + ') na (' + str(i) + ',' + str(k) + ')')
    return G


def barabasi_albert_graph(N=10, m=2, m0=None):
    G = nx.Graph()

    m0 = m0 if m0 is not None else m
    nodes = [i for i in range(m0)]
    G.add_nodes_from(nodes)

    # starting connections
    for i in range(m0):
        for j in range(i + 1, m0):
            G.add_edge(nodes[i], nodes[j])

    probs = [p / (2 * G.number_of_edges()) for p in G.degree(nodes).values()]
    for k in range(m0, N - m0):
        G.add_node(k)
        # add edges
        subset_of_nodes = choices(population=nodes, weights=probs, k=m)
        G.add_edges_from(zip([k] * m, subset_of_nodes))

        nodes = list(G.node.keys())  # nodes.append(k)
        probs = [p / (2 * G.number_of_edges()) for p in G.degree(nodes).values()]

    return G


def save_graph(G, path):
    # dot_graph = pd.graph_from_edges(list(G.edges()))
    # dot_graph.write(path)
    pickle.dump(G, open(path, 'wb'))


def read_graph(path):
    return pickle.load(open(path, 'rb'))


def draw_graph(G, to_png=True):
    # nx.draw_networkx(G, with_labels=True)
    # nx.draw_circular(G)
    if to_png:
        plt.savefig("graph.png", format="png")


def report(G, graph_type):
    print('Number of vertices: %d' % G.number_of_nodes())
    print('Number of edges: %d' % G.number_of_edges())

    degrees = list(G.degree().values())
    mean = numpy.mean(degrees)
    variance = numpy.var(degrees)

    print('Average degree: %g' % mean)
    print('Variance of degree distribution: %g' % variance)

    x = numpy.linspace(numpy.min(degrees), numpy.max(degrees), 100)
    log = False

    if graph_type == 'rand':
        plt.plot(x, mlab.normpdf(x, mean, numpy.sqrt(variance)), 'r-')

    elif graph_type == 'ws':
        y = [mean ** i * numpy.exp(-mean) / numpy.math.factorial(i) for i in numpy.round(x)]
        plt.plot(x, y, 'r')

    elif graph_type == 'ba':
        fit = powerlaw.Fit(degrees)

        # print('alpha = ' + str(fit.alpha))
        y = [200 * i ** (-fit.alpha) for i in x]
        plt.loglog(x, y, 'r-')
        log = True

    plot_hist(degrees, log=log)


def plot_hist(degrees, log=False):
    plt.hist(degrees, normed=True, log=log)
    plt.xlabel('degrees')
    plt.ylabel('number of nodes')
    plt.show()


N = 200
P = [0.3, 0.5, 0.8]

print('\nRANDOM GRAPH\n')

for p in P:
    print('P = {}\n'.format(p))
    rg = random_graph(N, p)
    report(rg, 'rand')
    print('')

print('\nWATTS-STROGATZ GRAPH\n')

for p in P:
    for k in [2, 4, 10]:
        print('P = {}\n'.format(p))
        ws = watts_strogatz_graph(N, k, p)
        report(ws, 'ws')
        print('')

print('\nBARABASI-ALBERT GRAPH\n')

for m0, m in [(2, 1), (2, 2), (10, 2), (10, 10)]:
    print('m0 = {}, m = {}\n'.format(m0, m))
    ba = barabasi_albert_graph(N, m, m0)
    report(ba, 'ba')
    print('')
