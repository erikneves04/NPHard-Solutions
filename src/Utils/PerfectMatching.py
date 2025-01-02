import networkx as nx

class PerfectMatching:
    def __find_odd_nodes(self, mst):
        degree = {}
    
        for u, v, _ in mst:
            if u not in degree:
                degree[u] = 0
            if v not in degree:
                degree[v] = 0
                
            degree[u] += 1
            degree[v] += 1

        return [vertex for vertex, deg in degree.items() if deg % 2 != 0]

    def BuildPerfectMathing(self, graph, mst):
        odd_vertices = self.__find_odd_nodes(mst)
        G = nx.Graph()

        for i in odd_vertices:
            for j in odd_vertices:
                if i != j:
                    G.add_edge(i, j, weight=graph[i][j])

        matching = nx.algorithms.matching.min_weight_matching(G)
        return [(u, v, G[u][v]['weight']) for u, v in matching]