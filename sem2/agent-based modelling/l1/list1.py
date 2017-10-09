from forest_fire import *
import matplotlib.pyplot as plt


# 1 tree; 2 fire; 0 empty; 3 burned tree


def check_if_fire_hit_other_side(forest):
    for cell in forest[-1]:
        if cell == 3:
            return 1
    return 0


def probability_that_fire_hits_other_side(p, L=20, MC=10):
    ans = 0.
    for mc in range(MC):
        f = forest_fire(p, L)
        ans += check_if_fire_hit_other_side(f)
    return ans / MC


def percolation_threshold(L, P, MC=10):
    res = np.zeros(len(P))
    i = 0
    for p in P:
        res[i] = probability_that_fire_hits_other_side(p, L, MC)
        i += 1
    plt.plot(P, res)
    plt.title('Percolation threshold')
    plt.xlabel('p')
    plt.ylabel('hit probability')
    plt.savefig('percolation' + str(L))


def hoshen_kopelman_alg(forest=np.array([])):
    # print_forest(forest)
    L = forest.shape[0]
    label_no = 0
    labels = np.zeros([L, L])
    for x, y in np.ndindex(forest.shape):
        if forest[x][y] == 3:
            above = forest[x - 1][y] if 0 <= x - 1 else 0
            left = forest[x][y - 1] if 0 <= y - 1 else 0

            if above == 0 and left == 0:
                label_no += 1
                labels[x][y] = label_no
            elif above == 3 and left == 0:
                labels[x][y] = labels[x - 1][y]
            elif above == 0 and left == 3:
                labels[x][y] = labels[x][y - 1]
            elif above == 3 and left == 3:  # above and left both have labels (different)
                if labels[x - 1][y] != labels[x][y - 1]:
                    union(labels, labels[x - 1][y], labels[x][y - 1])
                labels[x][y] = labels[x - 1][y]
    # count labels
    end_labels = [*labels.flatten()]
    biggest_cluster = dict((x, end_labels.count(x)) for x in set(end_labels) - {0})
    # return number of nodes in the biggest cluster
    # B = max(biggest_cluster.values() if len([*biggest_cluster.keys()]) > 0 else 0)
    if len(biggest_cluster) > 0:
        B = max(biggest_cluster.values())
    else:
        B = 0
    return B


def union(labels, l1, l2):
    """Change all labels l2 to l1"""
    for x, y in np.ndindex(labels.shape):
        if labels[x][y] == l2:
            labels[x][y] = l1


def avg_biggest_cluster(L, P, MC=10):
    # hoshen_kopelman for L=100, monte carlo for different p
    tmp = np.zeros(MC)
    res = []
    for p in P:
        for mc in range(MC):
            f = forest_fire(p, L)
            tmp[mc] = hoshen_kopelman_alg(f)
        res.append(tmp.mean())
    plt.plot(P, res)
    plt.title('Biggest cluster of burned trees for grid size = ' + str(L))
    plt.xlabel('p')
    plt.ylabel('number of trees')
    plt.savefig('biggest_cluster_L100')


if __name__ == "__main__":
    # print(percolation_threshold(0.5, 5, 10))
    # f = forest_fire(0.5, 5)
    # print(hoshen_kopelman_alg(f))
    L = 10
    P = [x for x in np.arange(0, 1., .1)]

    for l in [20, 50, 100]:
        percolation_threshold(L=l, P=P, MC=10)
    avg_biggest_cluster(L=L, P=P, MC=10)
