import random as rnd
from timeit import default_timer as timer

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def new_graph(g, N, M):
    if g == 'complete':
        return nx.complete_graph(N)
    elif g == 'ba':
        return nx.barabasi_albert_graph(N, M)


def MCsimulations(g, M, f, P, T=100, MC=1):
    N = 100
    q = 4
    c = np.zeros(len(P), float)

    for en, p in enumerate(P):
        final_c = 0
        for _ in range(MC):
            G = new_graph(g, N, M)
            votes = np.ones(N, int)

            for i in range(T):
                for _ in range(N):
                    voter = rnd.randint(0, N - 1)

                    if rnd.random() < p:  # independent
                        if rnd.random() < f:
                            votes[voter] = - votes[voter]
                    else:  # conformist
                        neighbours = [n for n in G.neighbors(voter)]
                        subset_votes = [votes[rnd.choice(neighbours)] for _ in range(q)]
                        if abs(sum(subset_votes)) == q:
                            votes[voter] = subset_votes[0]

            final_c += sum(votes) / N

        c[en] = final_c / MC
    return c


def situation_model_M(P, MC, rep):
    # MM = [2, 3, 4, 6, 8, 10]
    MM = [3, 6, 10]
    f = 0.5

    plt.figure()
    for M in MM:
        start = timer()
        res = MCsimulations('ba', M, f, P, MC, rep)
        print(M)
        print(timer() - start)
        plt.plot(P, res, '.')

    res = MCsimulations('complete', 0, f, P, MC, rep)
    plt.plot(P, res, '.')

    legend = ["M=" + str(M) for M in MM] + ['CG']
    plt.legend(legend)
    plt.xlabel("p")
    plt.ylabel("c")
    plt.title("Concentration of adopted c in the stationary state")
    plt.savefig("situation_M.png")
    plt.close()


def situation_model_f(P, T, MC):
    M = 4
    F = np.arange(0.2, 0.6, 0.1)

    plt.figure()
    for f in F:
        start = timer()
        res = MCsimulations('complete', M, f, P, T, MC)
        print(f)
        print(timer() - start)
        plt.plot(P, res, '.')

    legend = ["f=" + str(f) for f in F]
    plt.legend(legend)
    plt.xlabel("p")
    plt.ylabel("c")
    plt.title("Concentration of adopted c in the stationary state")
    plt.savefig("situation_f.png")
    plt.close()


if __name__ == "__main__":
    T = 100
    MC = 10
    P = np.arange(0., 1, 0.01)

    start = timer()
    print("M:")
    situation_model_M(P, T, MC)
    print(timer() - start)

    start = timer()
    print("f:")
    situation_model_f(P, T, MC)
    print(timer() - start)
