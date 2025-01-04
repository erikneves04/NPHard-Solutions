import networkx as nx
import numpy as np

class TwiceAroundTheTree:
    def __init__(self):
        self.graph = None
        
    def __mst_prim(self):
        return nx.minimum_spanning_tree(self.graph)
    
    def __hamiltonian_circuit(self, mstPrim):
        path = list(nx.dfs_preorder_nodes(mstPrim, 0))
        h_cycle = path + [path[0]]
        solution_aprox = 0
        for i in range(len(h_cycle) - 1):
            u, v = h_cycle[i], h_cycle[i+1]
            solution_aprox += self.graph[u][v]['weight']
        
        return solution_aprox, h_cycle  
    
    def __estimate_space_required__(self, graph, mst, hamiltonian_circuit):
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
        self.graph = nx.from_numpy_array(graph)
        mst_prim = self.__mst_prim()
        solution, hamitonian = self.__hamiltonian_circuit(mst_prim)                  
        
        space_required = self.__estimate_space_required__(graph, mst_prim, hamitonian)

        return solution, space_required
    