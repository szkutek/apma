import networkx as nx
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import pylab
from timeit import default_timer as timer


def new_graph(g, N, M):
    if g == 'complete':
        return nx.complete_graph(N)
    elif g == 'ba':
        return nx.barabasi_albert_graph(N, M)


def MCsimulations(g, M, f, P, MC=100, MC2=1):
    N = 100
    q = 4
    magnP = np.zeros(len(P), float)

    for en, p in enumerate(P):
        final_magn = 0
        for _ in range(MC2):
            G = new_graph(g, N, M)
            votes = np.ones(N, int)

            for i in range(MC - 1):
                for _ in range(N - 1):
                    voter = rnd.randint(0, N - 1)

                    if rnd.random() < p:  # independent
                        if rnd.random() < f:
                            votes[voter] = - votes[voter]
                    else:  # conformist
                        neighbours = [n for n in G.neighbors(voter)]
                        subset_votes = [votes[rnd.choice(neighbours)] for _ in range(q)]
                        if abs(sum(subset_votes)) == q:
                            votes[voter] = subset_votes[0]

            final_magn += sum(votes) / N

        magnP[en] = final_magn / MC2
    return magnP


def situation_model_M(P, MC, rep):
    MM = [2, 3, 4, 6, 8, 10]
    # MM = [10]
    f = 0.5

    plt.figure()
    for M in MM:
        res = MCsimulations('ba', M, f, P, MC, rep)
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


def situation_model_f(P, MC, rep):
    M = 4
    F = np.arange(0.2, 0.6, 0.1)

    plt.figure()
    for f in F:
        res = MCsimulations('ba', M, f, P, MC, rep)
        plt.plot(P, res, '.')

    legend = ["f=" + str(f) for f in F]
    plt.legend(legend)
    plt.xlabel("p")
    plt.ylabel("c")
    plt.title("Concentration of adopted c in the stationary state")
    plt.savefig("situation_f.png")
    plt.close()


if __name__ == "__main__":
    MC = 1000
    rep = 1000
    P = np.arange(0.1, 1, 0.02)

    start = timer()

    print("M:")
    situation_model_M(P, MC, rep)
    print(timer() - start)

    start = timer()
    print("f:")
    situation_model_f(P, MC, rep)
    print(timer() - start)
