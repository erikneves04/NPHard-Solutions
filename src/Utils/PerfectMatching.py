import networkx as nx

class PerfectMatching:
    """
    Classe responsável por encontrar o emparelhamento perfeito mínimo no grafo,
    considerando os vértices de grau ímpar na Árvore Geradora Mínima (MST).
    """

    def __find_odd_nodes(self, mst):
        """
        Encontra os vértices de grau ímpar na Árvore Geradora Mínima (MST).

        Parâmetros:
        - mst (List[Tuple[int, int, float]]): Lista de arestas na MST, onde cada aresta
          é representada como (u, v, peso).

        Retorno:
        - List[int]: Lista de vértices com grau ímpar.
        """
        
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
        """
        Constrói o emparelhamento perfeito mínimo para os vértices de grau ímpar na MST.

        Parâmetros:
        - graph (List[List[float]]): Matriz de adjacência representando o grafo completo.
        - mst (List[Tuple[int, int, float]]): Lista de arestas na MST, onde cada aresta
          é representada como (u, v, peso).

        Retorno:
        - List[Tuple[int, int, float]]: Lista de arestas no emparelhamento perfeito,
          onde cada aresta é representada como (u, v, peso).
        """

        odd_vertices = self.__find_odd_nodes(mst)

        G = nx.Graph()
        for i in odd_vertices:
            for j in odd_vertices:
                if i != j:
                    G.add_edge(i, j, weight=graph[i][j])

        matching = nx.algorithms.matching.min_weight_matching(G)

        return [(u, v, G[u][v]['weight']) for u, v in matching]
