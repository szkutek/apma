"""
Agnieszka Szkutek, 208619
"""

import networkx as nx
from urllib.request import urlopen
import matplotlib.pyplot as plt
import pickle


def save_graph(G, path):
    pickle.dump(G, open(path, 'wb'))


def read_graph(path):
    return pickle.load(open(path, 'rb'))


def get_friends(g, name):
    # fetch list of friends
    response = urlopen('http://www.livejournal.com/misc/fdata.bml?user=' + name)

    for line in response.readlines():
        if line.startswith(b'#'):
            continue

        # '< name' incoming or '> name' outgoing
        parts = line.split()
        if len(parts) == 0:
            continue

        # add edge to graph
        if parts[0] == '<':
            g.add_edge(parts[1].decode("utf-8"), name)
        else:
            g.add_edge(name, parts[1].decode("utf-8"))


def snowball_sampling(g, name, max_depth=1, current_depth=0, visited=[]):
    if current_depth == max_depth or name in visited:
        return visited
    else:
        visited.append(name)
    get_friends(g, name)
    for node in g.neighbors(name):
        visited = snowball_sampling(g, node, max_depth, current_depth + 1, visited)
    return visited


def sort_list_of_tuples(list):
    return sorted(list, key=lambda x: x[1], reverse=True)


def trim_degrees(g, degree=1):
    g2 = g.copy()
    d = nx.degree(g2)
    for n in g2.nodes():
        if d[n] <= degree:
            g2.remove_node(n)
    return g2


"""
FETCH DATA FROM LIVE JOURNAL

g = nx.DiGraph()
# get_friends(g, 'valerois')
snowball_sampling(g, 'valerois', 2)
save_graph(g, 'friends_of_valerois')
"""

g = read_graph('friends_of_valerois')
print('Number of nodes: {}'.format(g.number_of_nodes()))
print('Number of edges: {}'.format(g.number_of_edges()))
print('')

"""
CELEBRITIES
"""
deg = nx.degree_centrality(g)

deg_sorted_tuples = sort_list_of_tuples(list(deg.items()))
celebrities, cel_degree = zip(*deg_sorted_tuples)

print('Celebrities of the network: ')
print(celebrities[:10])
# print(deg_sorted_tuples[:3])
print('')

"""
DEGREE DISTRIBUTION
"""
plt.hist(list(deg.values()), 100)
plt.title('Degree distribution')
plt.xlabel('degree')
plt.ylabel('number of nodes')
plt.show()

plt.hist(list(deg.values()), 100, log=True)
plt.title('Degree distribution in loglog scale')
plt.xlabel('degree')
plt.ylabel('number of nodes')
plt.show()

"""
COMMUNICATION BOTTLENECKS
"""
g2 = trim_degrees(g, 40)

btw_centr = nx.betweenness_centrality(g2)
btw_centr_sorted_tuples = sort_list_of_tuples(list(btw_centr.items()))
bottlenecks, centrality = zip(*btw_centr_sorted_tuples)

print('Biggest bottlenecks of the network (with removed unimportant nodes): ')
print(bottlenecks[:10])
# print(btw_centr_sorted_tuples[:3])
