import networkx as nx
import numpy as np
import random as rnd
import matplotlib.pyplot as plt

L = 4
g = nx.grid_2d_graph(L, L)
for i in range(L * L):
    g.add_edge(i, i - L - 1)
    g.add_edge(i, i - L)
    g.add_edge(i, i - L + 1)

    g.add_edge(i, i - 1)
    g.add_edge(i, i + 1)

    g.add_edge(i, i + L - 1)
    g.add_edge(i, i + L)
    g.add_edge(i, i + L + 1)

# nodes = g.nodes()
# for i in nodes:
#     if i < 0 or i >= L * L:
#         g.remove_node(i)
#     if i % L == 0:
#         if g.has_edge(i, i - 1 - L):
#             g.remove_edge(i, i - 1 - L)
#         if g.has_edge(i, i - 1):
#             g.remove_edge(i, i - 1)
#         if g.has_edge(i, i - 1 + L):
#             g.remove_edge(i, i - 1 + L)

# g = nx.grid_2d_graph(L, L, create_using=g)
pos = zip(g.nodes(), g.nodes())
nx.draw(g, pos=pos, with_labels=True)
plt.show()
