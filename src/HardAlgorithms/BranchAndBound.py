from ProblemManager.ProblemManager import ProblemManager
import numpy as np
import heapq

BESTCOST = float('inf')

class BranchAndBound:
    def __init__(self, graph, numNodes):
        self.problemManager = ProblemManager()
        self.graph = graph
        self.numNodes = numNodes
        self.solution = None
        self.Cost = 0        
        
    def bound(self, partialSolution, costPartialSolution):
        
        
        listMinCosts = []
        sumTwoMin = []
        for i in range(self.numNodes):
            self.graph[i, i] = BESTCOST
            
            if i in partialSolution:
                continue
                
            # print(np.partition(self.graph[i, :],2)[:2])        
            sumTwoMin = np.sum(np.partition(self.graph[i, :],2)[:2])
            # print(sumTwoMin)
            listMinCosts.append(float(sumTwoMin)) 
            
        # print(listMinCosts)          
        
        bound = sum(listMinCosts)/2 + costPartialSolution
        print(bound)
        
    def solve(self, problem_path):
        problem = self.problemManager.ReadProblem(problem_path)

        # TODO: Implementar esse algoritmo

        return None
    
def main():
    """
    Função principal para testar a implementação do Branch and Bound.
    """
    # Matriz de pesos (simétrica) com 10 vértices
    graph = np.array([
        [0, 29, 20, 21, 16, 31, 100, 12, 4, 31],
        [29, 0, 15, 17, 28, 40, 72, 31, 29, 40],
        [20, 15, 0, 12, 15, 25, 81, 22, 13, 31],
        [21, 17, 12, 0, 11, 15, 92, 18, 17, 23],
        [16, 28, 15, 11, 0, 15, 94, 24, 14, 26],
        [31, 40, 25, 15, 15, 0, 96, 30, 29, 13],
        [100, 72, 81, 92, 94, 96, 0, 60, 60, 70],
        [12, 31, 22, 18, 24, 30, 60, 0, 16, 22],
        [4, 29, 13, 17, 14, 29, 60, 16, 0, 28],
        [31, 40, 31, 23, 26, 13, 70, 22, 28, 0]
    ], dtype=float)  

    num_nodes = len(graph)

    # Instanciando o Branch and Bound
    Solve = BranchAndBound(graph, num_nodes)

    Solve.bound([-1,-1,-1], 0)


if __name__ == "__main__":
    main()
