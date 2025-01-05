import networkx as nx
class TwiceAroundTheTree:
    """
    Classe que implementa o algoritmo Twice-Around-The-Tree para resolver o problema do Caixeiro Viajante (TSP) de forma aproximada.
    """
    def __init__(self):
        """
        Inicializa a classe com o grafo vazio.
        """
        self.graph = None
        
    def __mst_prim(self):
        """
        Calcula a Árvore Geradora Mínima (MST) do grafo usando o algoritmo de Prim.

        :return: Grafo representando a MST.
        """
        return nx.minimum_spanning_tree(self.graph)
    
    def __hamiltonian_circuit(self, mst_prim):
        """
        Calcula o circuito Hamiltoniano aproximado baseado no MST.

        :param mst_prim: Grafo representando a MST.
        :return: Tupla contendo o custo do circuito Hamiltoniano aproximado e a ordem dos nós no circuito.
        """
        path = list(nx.dfs_preorder_nodes(mst_prim, source=0))
        h_cycle = path + [path[0]]
        solution_aprox = 0
        for i in range(len(h_cycle) - 1):
            u, v = h_cycle[i], h_cycle[i + 1]
            if self.graph.has_edge(u, v):
                solution_aprox += self.graph[u][v]['weight']
            else:
                solution_aprox += 1.0
        
        return solution_aprox, h_cycle
    
    def __estimate_space_required__(self, graph, mst, hamiltonian_circuit):
        """
        Estima o espaço total necessário para resolver o problema utilizando o algoritmo Twice-Around-The-Tree.

        :param graph: Matriz representando o grafo com as distâncias entre os nós.
        :param mst: Grafo representando a MST.
        :param hamiltonian_circuit: Lista representando o circuito Hamiltoniano aproximado.
        :return total_space: Espaço estimado total gasto.
        """
        num_nodes = len(graph)
        mst_edges = len(mst)
        hamiltonian_nodes = len(hamiltonian_circuit)
        
        # Aproximações do espaço (em bytes):
        space_per_node = 8 
        space_per_edge = 16
        
        # Espaço total (em bytes)
        total_space = (
            num_nodes * space_per_node + 
            mst_edges * space_per_edge + 
            hamiltonian_nodes * space_per_node 
        )
        return total_space
            
    def solve(self, graph):
        """
        Resolve o problema de TSP utilizando o algoritmo Twice Around the Tree.

        :param graph: Grafo com os dados do problema.
        :return solution: Solução ótima para o problema.
        :retunr space_required: Espaço total gasto nessa instância.
        """
        self.graph = nx.from_numpy_array(graph)
        mst_prim = self.__mst_prim()
        solution, hamitonian = self.__hamiltonian_circuit(mst_prim)     
         
        space_required = self.__estimate_space_required__(graph, mst_prim, hamitonian)

        return solution, space_required
    