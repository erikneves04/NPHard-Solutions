from ProblemManager.ProblemManager import ProblemManager
import networkx as nx
import numpy as np

class TwiceAroundTheTree:
    def __init__(self):
        self.problemManager = ProblemManager()
        self.graph = None
        self.hCycle = []
        self.solutionAprox = 0
        
    def mstPrim(self):
        return nx.minimum_spanning_tree(self.graph)
            
    def solve(self, problem_path):
        self.graph = nx.from_numpy_array(self.problemManager.ReadProblem(problem_path)[0])

        mstPrim = self.mstPrim()
        path = list(nx.dfs_preorder_nodes(mstPrim, 0))
        self.hCycle = path + [path[0]]
        
        for i in range(len(self.hCycle) - 1):
            u, v = self.hCycle[i], self.hCycle[i+1]
            self.solutionAprox += self.graph[u][v]['weight']            
        
        print(f"O caminho aproximado é: {self.hCycle}")
        print(f"O custo do caminho anterior é: {self.solutionAprox}. O custo é aproximado, o custo ótimo é: ")
    