import networkx as nx

from Utils.PrimAlgorithm import PrimAlgorithm
from Utils.PerfectMatching import PerfectMatching
from Utils.HamiltonianPriceCalculator import HamiltonianPriceCalculator

class Christofides:
    """
    Implementação do algoritmo de Christofides para resolver o problema do Caixeiro Viajante (TSP).
    """

    def __init__(self):
        """
        Inicializa a classe Christofides com os algoritmos auxiliares:
        - Algoritmo de Prim para construir a Árvore Geradora Mínima (MST).
        - Algoritmo de Emparelhamento Perfeito (Perfect Matching).
        """
        self.primAlgorithm = PrimAlgorithm()
        self.matchAlgorithm = PerfectMatching()

    def __find_eulerian_circuit(self, graph):
        """
        Encontra o circuito euleriano no grafo dado.

        Parâmetros:
        - graph (nx.Graph): Grafo com arestas duplicadas formando um grafo euleriano.

        Retorno:
        - List[Tuple[int, int]]: Lista de arestas que formam o circuito euleriano.
        """
        return list(nx.eulerian_circuit(graph))

    def __convert_to_hamiltonian_circuit(self, eulerian):
        """
        Converte o circuito euleriano em um circuito hamiltoniano.

        Parâmetros:
        - eulerian (List[Tuple[int, int]]): Circuito euleriano como uma lista de arestas.

        Retorno:
        - List[int]: Circuito hamiltoniano representado como uma lista de nós.
        """
        visited = set()
        hamiltonian_circuit = []

        for u, v in eulerian:
            if u not in visited:
                hamiltonian_circuit.append(u)
                visited.add(u)
        hamiltonian_circuit.append(hamiltonian_circuit[0])  
        
        return hamiltonian_circuit

    def __estimate_space_required__(self, graph, mst, matching, hamiltonian_circuit):
        """
        Estima o espaço em memória necessário para armazenar os componentes do algoritmo.

        Parâmetros:
        - graph (nx.Graph): Grafo de entrada.
        - mst (List[Tuple[int, int, float]]): Árvore Geradora Mínima (MST).
        - matching (List[Tuple[int, int, float]]): Emparelhamento perfeito.
        - hamiltonian_circuit (List[int]): Circuito hamiltoniano.

        Retorno:
        - int: Estimativa do espaço necessário em bytes.
        """
        num_nodes = len(graph)
        mst_edges = len(mst)
        matching_edges = len(matching)
        eulerian_edges = mst_edges + matching_edges
        hamiltonian_nodes = len(hamiltonian_circuit)
        
        # Aproximações do espaço (em bytes):
        space_per_node = 8 
        space_per_edge = 16
        
        # Espaço total (em bytes)
        total_space = (
            num_nodes * space_per_node + 
            eulerian_edges * space_per_edge + 
            hamiltonian_nodes * space_per_node 
        )
        return total_space

    def solve(self, graph):
        """
        Resolve o problema do Caixeiro Viajante (TSP) utilizando o algoritmo de Christofides.

        Parâmetros:
        - graph (nx.Graph): Grafo ponderado representando o problema do TSP.

        Retorno:
        - Tuple[float, int]: Solução do problema (custo do circuito hamiltoniano) e
          estimativa de espaço em memória necessário (em bytes).
        """

        # Construir a Árvore Geradora Mínima (MST)
        mst, _ = self.primAlgorithm.BuildMST(graph)

        # Construir o emparelhamento perfeito nos nós de grau ímpar
        matching = self.matchAlgorithm.BuildPerfectMathing(graph, mst)

        # Criar o grafo euleriano
        eulerian_graph = nx.MultiGraph()
        eulerian_graph.add_edges_from([(u, v, {'weight': w}) for u, v, w in mst + matching])
        
        # Encontrar o circuito euleriano
        eulerian = self.__find_eulerian_circuit(eulerian_graph)

        # Converter o circuito euleriano para um circuito hamiltoniano
        hamiltonian = self.__convert_to_hamiltonian_circuit(eulerian)

        # Calcular o custo do circuito hamiltoniano
        solution = HamiltonianPriceCalculator.Calculate(graph, hamiltonian)

        # Estimar o espaço necessário
        space_required = self.__estimate_space_required__(graph, mst, matching, hamiltonian)

        return solution, space_required