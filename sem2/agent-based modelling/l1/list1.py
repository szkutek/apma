from forest_fire import *
import matplotlib.pyplot as plt
from timeit import default_timer as timer


# 1 tree; 2 fire; 0 empty; 3 burned tree


def check_if_fire_hit_other_side(forest):
    for cell in forest[-1]:
        if cell == 3:
            return 1
    return 0


def probability_that_fire_hits_other_side(p, L=20, MC=10, Dir='0', Str=1):
    ans = 0.
    for mc in range(MC):
        f = forest_fire(p, L, Dir, Str)
        ans += check_if_fire_hit_other_side(f)
    return ans / MC


def percolation_threshold(L, P, MC=10, Dir='0', Strengths=list([1])):
    plt.close('all')
    if len(Strengths) > 1:
        fig, ax = plt.subplots(len(Strengths), sharex=True, sharey=True)  # ax is a tuple
        fig.set_size_inches(10, 10)
        fig.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
        plt.title('Percolation threshold for L = ' + str(L) + ', wind direction ' + Dir)
        plt.ylabel('hit probability')
        plt.xlabel('p')
        fig.subplots_adjust(hspace=0)

    s = 0
    for Str in Strengths:

        res = np.zeros(len(P))
        i = 0
        for p in P:
            res[i] = probability_that_fire_hits_other_side(p, L, MC, Dir=Dir, Str=Str)
            i += 1

        if len(Strengths) > 1:
            ax[s].plot(P, res)
            ax[s].set_title('wind strength = ' + str(Str), x=0.15, y=0.85)
            s += 1
        else:
            plt.plot(P, res)
            plt.title('Percolation threshold for L = ' + str(L))
            plt.xlabel('p')
            plt.ylabel('hit probability')
    if len(Strengths) > 1:
        plt.savefig('percolation_L' + str(L) + '_MC' + str(MC) + '_Dir' + str(Dir))
    else:
        plt.savefig('exercise1_L' + str(L) + '_MC' + str(MC))


def hoshen_kopelman_alg(forest=np.array([])):
    # print_forest(forest) TODO remove this print
    L = forest.shape[0]
    label_no = 0
    labels = np.zeros([L, L])
    for x, y in np.ndindex(forest.shape):
        if forest[x][y] == 3:
            above = forest[x - 1][y] if 0 <= x - 1 else 0
            left = forest[x][y - 1] if 0 <= y - 1 else 0

            if above != 3 and left != 3:
                label_no += 1
                labels[x][y] = label_no
            elif above == 3 and left != 3:
                labels[x][y] = labels[x - 1][y]
            elif above != 3 and left == 3:
                labels[x][y] = labels[x][y - 1]
            elif above == 3 and left == 3:  # above and left both have labels (burned tree)
                if labels[x - 1][y] != labels[x][y - 1]:
                    union(labels, labels[x - 1][y], labels[x][y - 1])
                labels[x][y] = labels[x - 1][y]

    final_labels = [*labels.flatten()]
    clusters = dict((x, final_labels.count(x)) for x in set(final_labels) - {0})  # count labels
    return max(clusters.values()) if len(clusters) > 0 else 0  # return number of nodes in the biggest cluster


def union(labels, l1, l2):
    """Change all labels l2 to l1"""
    for x, y in np.ndindex(labels.shape):
        if labels[x][y] == l2:
            labels[x][y] = l1


def avg_biggest_cluster(L, P, MC=10, Dir='0', Strengths=list([1])):
    """ hoshen_kopelman for L=100, monte carlo for different p """
    plt.close('all')
    if len(Strengths) > 1:
        fig, ax = plt.subplots(len(Strengths), sharex=True, sharey=True)  # ax is a tuple
        fig.set_size_inches(10, 10)
        fig.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
        plt.title('Biggest cluster of burned trees for L=' + str(L) + ', wind direction ' + Dir)
        plt.ylabel('number of trees')
        plt.xlabel('p')
        fig.subplots_adjust(hspace=0)

    s = 0
    for Str in Strengths:
        res = np.zeros(len(P))
        i = 0
        for p in P:
            tmp = 0.
            for _ in range(MC):
                f = forest_fire(p, L, Dir, Str)
                tmp += hoshen_kopelman_alg(f)
            res[i] = tmp / MC
            i += 1

        if len(Strengths) > 1:
            ax[s].plot(P, res)
            ax[s].set_title('wind strength = ' + str(Str), x=0.15, y=0.85)
            s += 1
        else:
            plt.plot(P, res)
            plt.title(
                'Biggest cluster of burned trees for L=' + str(L) + ', dir ' + Dir + ' and strength ' + str(Str))
            plt.xlabel('p')
            plt.ylabel('number of trees')

    if len(Strengths) > 1:
        plt.savefig('biggest_cluster_L100_MC' + str(MC) + '_Dir' + str(Dir))
    else:
        plt.savefig('exercise2')


if __name__ == "__main__":
    # print(percolation_threshold(0.5, 5, 10))
    # f = forest_fire(0.5, 5)
    # print(hoshen_kopelman_alg(f))
    MC = 20
    P = [x for x in np.arange(.0, 1.1, .1)]

    start = timer()

    # exercise 1
    Strength = [1]
    L = [20, 50, 100]
    d = '0'
    for l in L:
        percolation_threshold(L=l, P=P, MC=MC, Dir=d, Strengths=Strength)
        print('percolation for d=' + d + ', l=' + str(l))
        print(timer() - start)
    print('exercise 1 done\n')

    # exercise 2
    avg_biggest_cluster(L=L[-1], P=P, MC=MC, Dir=d, Strengths=Strength)
    print(timer() - start)
    print('exercise 2 done\n')

    # exercise 3
    l = 20
    Strength = [2, 10]
    Direction = ['N', 'W']

    for D in Direction:
        percolation_threshold(L=l, P=P, MC=MC, Dir=D, Strengths=Strength)
        print('percolation for d=' + D + ', l=' + str(l))
        print(timer() - start)
        print('')

        avg_biggest_cluster(L=l, P=P, MC=MC, Dir=D, Strengths=Strength)
        print('biggest cluster for d=' + D)
        print(timer() - start)
        print('')

    print('exercise 3 done\n')
