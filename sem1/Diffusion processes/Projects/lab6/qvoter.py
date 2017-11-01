"""
Agnieszka Szkutek, 208619
"""

import random as rnd
from timeit import default_timer as timer

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pylab


def save_graph(G, pathname, i):
    fig = pylab.figure()
    pos = nx.spring_layout(G)
    size = 200

    green = []
    red = []
    for node in G.nodes():
        if G.node[node]['vote']:
            green.append(node)
        else:
            red.append(node)

    nx.draw_networkx_nodes(G, pos, nodelist=green, node_color='g', node_size=size, alpha=0.8)
    nx.draw_networkx_nodes(G, pos, nodelist=red, node_color='r', node_size=size, alpha=0.8)

    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

    s = pathname + "_" + str(i) + ".png"
    pylab.savefig(s)
    pylab.close(fig)


def new_graph(g, N):
    if g == 'complete':
        return nx.complete_graph(N)
    elif g == 'ba':
        return nx.barabasi_albert_graph(N, 4)
    elif g == 'ws1':
        return nx.watts_strogatz_graph(N, 4, 0.01)
    elif g == 'ws2':
        return nx.watts_strogatz_graph(N, 4, 0.2)


def MCsimulations(plot_type, g, N, P, q=3, MC=100, MC2=1):
    """plot_type is either 'p' (m(p)) or 't' (m(t)) """

    if plot_type == 'p':
        return plot_type_p_MCsim(g, N, P, q, MC, MC2)
    elif plot_type == 't':
        return plot_type_t_MCsim(g, N, P, q, MC, MC2)


def plot_type_p_MCsim(g, N, P, q, MC, MC2):
    magnP = np.zeros(len(P))
    for i in range(len(P)):
        p = P[i]
        final_magn = 0
        for j in range(MC2):
            # timeline = one_timeline_simulation(g, N, p, q, MC)
            # final_magn += timeline[-1]

            G = new_graph(g, N)
            votes = np.ones(N, int)

            for k in range(MC):
                for l in range(N):
                    timeline_magn = qvoter_NNgroup(G, N, q, p, votes)

            final_magn += timeline_magn

        magnP[i] = final_magn / MC2
    return magnP


def plot_type_t_MCsim(g, N, P, q, MC, MC2):
    timeP = []
    for p in P:
        timeline0 = np.zeros(MC)
        for k in range(MC2):
            timeline = one_timeline_simulation(g, N, p, q, MC)
            timeline0 = np.add(timeline0, timeline)

        timeP.append(np.divide(timeline0, MC2))
    return timeP


def one_timeline_simulation(g, N, p, q, MC):
    G = new_graph(g, N)
    votes = np.ones(N, int)

    timeline = np.zeros(MC)
    timeline[0] = 1
    for i in range(MC - 1):
        for j in range(N - 1):
            qvoter_NNgroup(G, N, q, p, votes)
        timeline[i + 1] = qvoter_NNgroup(G, N, q, p, votes)

    return timeline


def qvoter_NNgroup(G, N, q, p, votes):  # zad1
    voter = rnd.randint(0, N - 1)

    if rnd.random() < p:  # independent
        if rnd.random() < 0.5:
            votes[voter] = - votes[voter]
    else:  # conformist
        subset = np.zeros(q, int)
        neighbours = G.neighbors(voter)

        for k in range(q):
            subset[k] = rnd.choice(neighbours)

        #####
        # sv_sum = 0
        # for node in subset:
        #     sv_sum += votes[node]
        #
        # if abs(sv_sum) == q:  # q-panel is unanimous
        #     votes[voter] = votes[subset[0]]
        first_vote = votes[subset[0]]
        i = 0
        while i < q and first_vote == votes[subset[i]]:
            i += 1
        if i == q:
            votes[voter] = first_vote

    return sum(votes) / N  # magnetization(N, votes)


def zad2(rep=1):
    N = 100
    MC = 1000
    Q = [3, 4]
    P = list(np.arange(0.0, 0.51, 0.02))
    for q in Q:
        t1 = MCsimulations('t', 'complete', N, P, q, MC=MC, MC2=rep)
        t2 = MCsimulations('t', 'bs', N, P, q, MC=MC, MC2=rep)
        t3 = MCsimulations('t', 'ws1', N, P, q, MC=MC, MC2=rep)
        t4 = MCsimulations('t', 'ws2', N, P, q, MC=MC, MC2=rep)


def zad3():
    zad2(100)


def zad4(N, MC, rep):
    Q = [3, 4]
    P_short = [0.0, 0.2, 0.5, 0.7]

    g = 'ws1'

    for q in Q:
        single_run_WS('t', g, N, P_short, q, MC, MC2=1, show=False)
        single_run_WS('t', g, N, P_short, q, MC, MC2=rep, show=False)

        # plt.show()


def final_magnetization(N, MC, rep, q):
    # TODO ustawic wiecej p w P
    P_long = np.arange(0.0, 0.5, 0.01)

    G = ['complete', 'ba', 'ws1', 'ws2']
    plt.figure()
    for g in G:
        m = MCsimulations('p', g, N, P_long, q, MC=MC, MC2=rep)
        plt.plot(P_long, m, '*-')
    plt.legend(['complete', 'BA(100,4)', 'WS(100,4,0.01)', 'WS(100,4,0.2)'])
    plt.xlabel("independence probability")
    plt.ylabel("final magnetization")
    plt.title("Final magnetization for different topologies with q=" + str(q))
    plt.savefig("final_magn_" + str(q))
    plt.close()


def zad5a(N, MC, rep):
    print("part 1:")
    final_magnetization(N, MC, rep, 3)
    print("part 2:")
    final_magnetization(N, MC, rep, 4)


def zad5b(N, MC, rep):
    # TODO ustawic wiecej p w P
    P_long = np.arange(0.0, 0.5, 0.05)
    Q = [3, 4]

    plt.figure()
    leg = []
    for q in Q:
        m = MCsimulations('p', 'ws1', N, P_long, q, MC=MC, MC2=rep)
        plt.plot(P_long, m, '*-')
        leg.append('q = ' + str(q))

    plt.legend(leg)
    plt.xlabel("independence probability")
    plt.ylabel("final magnetization")
    plt.title("Final magnetization for WS(100,4,0.01)")

    plt.savefig("final_magn_ws001")
    plt.close()


def single_run_WS(plot_type, graph, N, P, q, MC, MC2=1, show=True):
    plt.figure()

    if plot_type == 'p':
        m = MCsimulations(plot_type, graph, N, P, q, MC=MC, MC2=MC2)
        plt.plot(P, m, '*')
        plt.xlabel("independence probability")
    elif plot_type == 't':
        t = MCsimulations(plot_type, graph, N, P, q, MC=MC, MC2=MC2)
        for res in t:
            plt.plot(res)
        plt.legend(P, loc='upper right')
        plt.xlabel("time")

    plt.ylabel("magnetization")
    if MC2 == 1:
        plt.title("magnetization of WS(100,4,0.01), single run, q=" + str(q))
    else:
        plt.title("magnetization of WS(100,4,0.01), average, q=" + str(q))

    if show:
        plt.show()
    else:
        plt.savefig("zad4_q=" + str(q) + "_rep=" + str(MC2) + ".png")


if __name__ == "__main__":
    # N = 100
    # MC = 1000
    # rep = 100

    N = 100
    MC = 10
    rep = 10

    start = timer()

    zad4(N, MC, rep)
    print("koniec zad 4")

    zad5a(N, MC, rep)
    print("koniec zad 5a")

    zad5b(N, MC, rep)
    print("koniec zad 5b")
    print(timer() - start)
