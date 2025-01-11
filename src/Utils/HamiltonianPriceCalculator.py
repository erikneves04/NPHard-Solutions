class HamiltonianPriceCalculator:
    """
    Classe responsável por calcular o custo total de um circuito hamiltoniano em um grafo.
    """

    @staticmethod
    def Calculate(graph, path):
        """
        Calcula o custo total de um caminho hamiltoniano em um grafo.

        Parâmetros:
        - graph (List[List[float]]): Matriz de adjacência representando o grafo completo.
        - path (List[int]): Lista de vértices representando o circuito hamiltoniano,
          onde o primeiro e o último vértice são iguais.

        Retorno:
        - float: O custo total do circuito hamiltoniano, somando os pesos das arestas
          no caminho especificado.
        """
        
        total = 0

        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            total += graph[u][v]
        
        return total