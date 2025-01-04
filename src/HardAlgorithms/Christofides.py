import networkx as nx

from Utils.PrimAlgorithm import PrimAlgorithm
from Utils.PerfectMatching import PerfectMatching
from Utils.HamiltonianPriceCalculator import HamiltonianPriceCalculator
from ProblemManager.ProblemManager import ProblemManager

class Christofides:
    def __init__(self):
        self.problemManager = ProblemManager()
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

    def solve(self, problem):
        graph, _ = self.problemManager.ReadProblem(problem)

        mst, _ = self.primAlgorithm.BuildMST(graph)
        matching = self.matchAlgorithm.BuildPerfectMathing(graph, mst)

        eulerian_graph = nx.MultiGraph()
        eulerian_graph.add_edges_from([(u, v, {'weight': w}) for u, v, w in mst + matching])
        
        eulerian = self.__find_eulerian_circuit(eulerian_graph)
        hamiltonian = self.__convert_to_hamiltonian_circuit(eulerian)

        print(f'Price: {HamiltonianPriceCalculator.Calculate(graph, hamiltonian)}')
        return hamiltonian