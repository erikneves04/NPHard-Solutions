class PrimAlgorithm:
    def BuildMST(self, graph):
        """
        Finds the Minimum Spanning Tree (MST) using Prim's Algorithm.
        :return: A list of edges in the MST and the total weight.
        :param adjacency_matrix: A square numpy array representing the graph.
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