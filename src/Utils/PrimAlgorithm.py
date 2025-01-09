class PrimAlgorithm:
    def BuildMST(self, graph):
        """
        Encontra a Árvore Geradora Mínima (MST) usando o Algoritmo de Prim.
        :return: Uma lista de arestas na MST e o peso total.
        :param adjacency_matrix: Um array quadrado do numpy representando o grafo.
        """

        self.graph = graph
        self.num_nodes = graph.shape[0]
        selected_nodes = [False] * self.num_nodes
        mst_edges = []  # (u, v, weight)
        total_weight = 0

        selected_nodes[0] = True
        for _ in range(self.num_nodes - 1):
            min_weight = float('inf')
            u, v = -1, -1

            for i in range(self.num_nodes):
                if selected_nodes[i]:
                    for j in range(self.num_nodes):
                        if not selected_nodes[j] and 0 < self.graph[i][j] < min_weight:
                            min_weight = self.graph[i][j]
                            u, v = i, j

            if u != -1 and v != -1:
                selected_nodes[v] = True
                mst_edges.append((u, v, min_weight))
                total_weight += min_weight

        return mst_edges, total_weight