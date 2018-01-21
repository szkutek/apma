import random as rnd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def MCsimulations(G, p, q, T):
    N = G.number_of_nodes()
    result = np.zeros(T + 1)
    result[0] = 0
    votes = np.ones(N, int)

    for i in range(T):
        for _ in range(N):
            voter = rnd.randint(0, N - 1)
            if rnd.random() < p:  # independent
                votes[voter] = -1
            else:  # conformist
                subset_votes = [votes[n] for n in G.neighbors(voter)]
                if rnd.random() < q * subset_votes.count(-1) / N:
                    votes[voter] = -1
        result[i + 1] = (votes == -1).sum() / N
    return result


def bass_model_p(G, T):
    q = 0.3
    P = [0.01, 0.02, 0.03, 0.1]

    plt.figure()
    for p in P:
        res = MCsimulations(G, p, q, T)
        plt.plot(range(T + 1), res)

    legend = ["p=" + str(p) for p in P]
    plt.legend(legend)
    plt.xlabel("time")
    plt.ylabel("F(t)")
    plt.title("")
    plt.savefig("bass_p.png")
    plt.close()


def bass_model_q(G, T):
    p = 0.01
    Q = [0.3, 0.4, 0.5]

    plt.figure()
    for q in Q:
        res = MCsimulations(G, p, q, T)
        plt.plot(range(T + 1), res)

    legend = ["q=" + str(q) for q in Q]
    plt.legend(legend)
    plt.xlabel("time")
    plt.ylabel("F(t)")
    plt.title("")
    plt.savefig("bass_q.png")
    plt.close()


if __name__ == "__main__":
    T = 30
    N = 500
    g = nx.complete_graph(N)

    print('p:')
    bass_model_p(g, T)
    print('q:')
    bass_model_q(g, T)
