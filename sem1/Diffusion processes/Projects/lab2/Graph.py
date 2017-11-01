class Vertex:
    def __init__(self, name):
        self.name = name
        self.neighbours = dict()  # {node: weight}

    def addNeighbour(self, vert, weight):
        self.neighbours[vert] = weight


class Graph:
    default_weight = 1

    def __init__(self):
        self.vertices = dict()  # {'a':Vertex('a')}

    def __str__(self):
        return self.getEdges()

    def __contains__(self, v):
        return v in self.vertices.keys()

    def addVertex(self, vert):
        if vert not in self.vertices.keys():
            self.vertices[vert] = Vertex(vert)

    def addVerticesFromList(self, vertList):
        for v in vertList:
            self.addVertex(v)

    def addEdge(self, fromVert, toVert, weight=default_weight):
        if fromVert == toVert:
            return
        self.addVerticesFromList([fromVert, toVert])

        self.vertices[fromVert].addNeighbour(toVert, weight)
        self.vertices[toVert].addNeighbour(fromVert, weight)

    def addEdgesFromList(self, edgeList):
        for e in edgeList:
            if len(e) == 2:
                self.addEdge(e[0], e[1])
            else:
                self.addEdge(e[0], e[1], e[2])

    def getVertices(self):
        return list(self.vertices.keys())

    def getEdges(self):
        edges = []
        for v in self.vertices.keys():
            for n in self.vertices[v].neighbours.keys():
                if (v, n, self.vertices[v].neighbours[n]) not in edges and \
                                (n, v, self.vertices[v].neighbours[n]) not in edges:
                    edges.append((v, n, self.vertices[v].neighbours[n]))
                    # if (v, n) not in edges and (n, v) not in edges:
                    #     edges.append((v, n))
        return edges

    def getNeighbors(self, vertKey):
        return list(self.vertices[vertKey].neighbours.keys())

    def saveGraph(self):  # tab z listy1
        edges = self.getEdges()
        f = open('graph.txt', 'w')
        f.write('graph G {\n')
        for i in edges:
            f.write(str(i[0]) + ' -- ' + str(i[1]) + ' [label = ' + str(i[2]) + ']\n')
        for i in self.vertices.keys():
            if len(self.getNeighbors(i)) == 0:
                f.write(str(i) + '\n')
        f.write('}\n')

    def shortestDistances(self, fromVert):
        dist = {fromVert: 0}
        prev = {}
        V = self.getVertices()

        for k in range(len(V)):
            # search for node with minimum dist
            min_dist_node = None
            for u in V:
                if u in dist:
                    if min_dist_node is None or dist[u] < dist[min_dist_node]:
                        min_dist_node = u
            if min_dist_node is None:
                break

            V.remove(min_dist_node)
            current_weight = dist[min_dist_node]

            Neighbours = self.vertices[min_dist_node].neighbours
            for w in Neighbours:
                weight = current_weight + Neighbours[w]
                if w not in dist or dist[w] > weight:
                    dist[w] = weight
                    prev[w] = min_dist_node
        return dist, prev

    def getShortestPaths(self, fromVert):
        dist, prev = self.shortestDistances(fromVert)

        # shortestPaths('a'): {(a,c): [[a,b,c], len]}
        path = {(fromVert, key): [[], None] for key in self.getVertices()}
        path.pop((fromVert, fromVert))
        for k, v in prev.items():
            path[(fromVert, k)][1] = dist[k]

            path[(fromVert, k)][0].append(v)
            path[(fromVert, k)][0].append(k)
            while v in prev.keys():
                v = prev[v]
                path[(fromVert, k)][0].insert(0, v)

        return path


if __name__ == '__main__':

    zwykly = 1

    if zwykly:
        g = Graph()

        g.addVertex('a')
        g.addVertex('g')
        g.addVertex(3)
        g.addVertex(-2)
        g.addVertex('b')
        g.addVerticesFromList(['b', 'c'])
        g.addVerticesFromList(['g', 'c'])
        g.addVerticesFromList(['a', 'c'])
        g.addVerticesFromList(['c', 'd'])
        print(g.getVertices())
        print("'a' in g: ", 'a' in g)

        g.addEdge('a', 'b', 3)
        g.addEdge('a', 'c')
        g.addEdge('c', 'd', 2)
        g.addEdge('c', 'a', 2)
        # print(g.__str__())
        print(g.getEdges())
        print(g.getNeighbors('c'))
        # g.saveGraph()
        print(g.getShortestPaths('a'))

    if not zwykly:
        p = Graph()
        p.addEdgesFromList([['A', 'B'], ['A', 'C'], ['A', 'D'], ['A', 'E'], ['A', 'F'],
                            ['G', 'B'], ['G', 'H'], ['H', 'I'], ['H', 'J'], ['G', 'J'],
                            ['I', 'G'], ['I', 'J'], ['E', 'F'], ['C', 'D'], ['C', 'F']])

        print(p.getVertices())
        print(p.getEdges())
        print(p.getNeighbors('I'))
        print(p.getShortestPaths('I'))
