import networkx as nx

from Utils.PrimAlgorithm import PrimAlgorithm
from Utils.PerfectMatching import PerfectMatching
from Utils.HamiltonianPriceCalculator import HamiltonianPriceCalculator

class Christofides:
    def __init__(self):
        self.primAlgorithm = PrimAlgorithm()
        self.matchAlgorithm = PerfectMatching()

    def __find_eulerian_circuit(self, graph):
        return list(nx.eulerian_circuit(graph))

    def __convert_to_hamiltonian_circuit(self, eulerian):
        visited = set()
        hamiltonian_circuit = []

        for u, v in eulerian:
            if u not in visited:
                hamiltonian_circuit.append(u)
                visited.add(u)
        hamiltonian_circuit.append(hamiltonian_circuit[0])  
        
        return hamiltonian_circuit

    def __estimate_space_required__(self, graph, mst, matching, hamiltonian_circuit):
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
        mst, _ = self.primAlgorithm.BuildMST(graph)
        matching = self.matchAlgorithm.BuildPerfectMathing(graph, mst)

        eulerian_graph = nx.MultiGraph()
        eulerian_graph.add_edges_from([(u, v, {'weight': w}) for u, v, w in mst + matching])
        
        eulerian = self.__find_eulerian_circuit(eulerian_graph)
        hamiltonian = self.__convert_to_hamiltonian_circuit(eulerian)
        solution = HamiltonianPriceCalculator.Calculate(graph, hamiltonian)

        space_required = self.__estimate_space_required__(graph, mst, matching, hamiltonian)

        return solution, space_required