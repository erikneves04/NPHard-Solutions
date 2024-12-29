from ProblemManager.ProblemManager import ProblemManager
import networkx as nx
import numpy as np

class TwiceAroundTheTree:
    def __init__(self, graph):
        self.problemManager = ProblemManager()
        self.graph = graph
        self.hCycle = []
        self.solutionAprox = 0
        
    def mstPrim(self):
        return nx.minimum_spanning_tree(self.graph, algorithm='prim', weight='weight')
            
    def solve(self, problem_path):
        # problem = self.problemManager.ReadProblem(problem_path)

        mstPrim = self.mstPrim()
        path = list(nx.dfs_preorder_nodes(mstPrim, 0))
        self.hCycle = path + [path[0]]
        
        for i in range(len(self.hCycle) - 1):
            u, v = self.hCycle[i], self.hCycle[i+1]
            self.solutionAprox += self.graph[u][v]['weight']
            
        print("Ciclo Hamiltoniano:", self.hCycle)
        print("Custo total do ciclo:", self.solutionAprox)         
        
        return self.hCycle, self.solutionAprox
    
def main():
    graph = np.array([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ], dtype=float) 
    
    graph = nx.from_numpy_array(graph)

    Solve = TwiceAroundTheTree(graph)
    
    path, cost = Solve.solve(0)
    print(f"O caminho de solução aproximada é: {path}")
    print(f"O custo do caminho é: {cost}")
    
if __name__ == "__main__":
    main()
