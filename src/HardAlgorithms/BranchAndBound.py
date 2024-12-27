from ProblemManager.ProblemManager import ProblemManager
import numpy as np
import heapq
import math

BESTCOST = float('inf')
class BranchAndBound:
    def __init__(self, graph, numNodes):
        self.problemManager = ProblemManager()
        self.graph = graph
        self.numNodes = numNodes
        self.solution = None
        self.bestCost  = BESTCOST     
        self.prunes = 0
        self.iter = 0
        
    def bound(self, partialSolution, costPartialSolution):      
        listMinCosts = []
        usedCosts = {v: set() for v in range(self.numNodes)}  
        # print(f"Partial Solution: {partialSolution}")
        # print(f"Cost Partial Solution: {costPartialSolution}")

        for idx in range(len(partialSolution)):
            current = partialSolution[idx]
            prev = partialSolution[idx - 1] if idx > 0 else None
            next_ = partialSolution[idx + 1] if idx + 1 < len(partialSolution) else None

            # print(f"Processing vertex {current}, prev: {prev}, next: {next_}")
            if prev is not None:
                costPrev = float(self.graph[current, prev])  
                listMinCosts.append(costPrev)
                usedCosts[current].add(costPrev)  
                # print(f"Cost to previous vertex ({prev}): {costPrev}")
            if next_ is not None:
                costNext = float(self.graph[current, next_]) 
                listMinCosts.append(costNext)
                usedCosts[current].add(costNext)  
                # print(f"Cost to next vertex ({next_}): {costNext}")

        for i in range(self.numNodes):
            if len(usedCosts[i]) >= 2:
                # print(f"Vertex {i} fully processed, skipping.")
                continue  

            # print(f"Processing remaining vertex {i}.")
            row = self.graph[i, :]  
            row[i] = BESTCOST 

            validCosts = [float(cost) for cost in row if cost not in usedCosts[i]]
            if not validCosts:
                # print(f"No valid costs remaining for vertex {i}. Skipping.")
                continue

            if len(usedCosts[i]) == 1:
                minCost = np.partition(validCosts, 0)[0]
            else:
                minCost = np.partition(validCosts, 1)[:2]

            if isinstance(minCost, np.ndarray):
                for cost in minCost:
                    usedCosts[i].add(cost)
                sumCosts = float(np.sum(minCost)) 
            else:
                usedCosts[i].add(minCost)
                sumCosts = float(minCost)

            listMinCosts.append(sumCosts)
            # print(f"Valid costs for vertex {i}: {validCosts}")
            # print(f"Smallest costs for vertex {i}: {minCost}")
            # print(f"Sum of costs added for vertex {i}: {sumCosts}")

        # print(f"\nList of minimum costs: {listMinCosts}")
        bound = math.ceil(np.sum(listMinCosts) / 2) # Converte o resultado final
        # print(f"Calculated bound: {bound}")
        return bound
        
    def brandAndBound(self, partialSolution, costPartialSolution):
        self.iter += 1
        print(f"Partial Solution: {partialSolution}")
        
        if len(partialSolution) == self.numNodes:
            startVertex = partialSolution[0]
            endVertex = partialSolution[-1]
            totalCost = costPartialSolution + self.graph[endVertex, startVertex]
            
            if totalCost < self.bestCost:
                self.bestCost = totalCost
                self.solution = partialSolution[:]
            else:
                print("podou")
                self.prunes += 1
            return
                    
        for i in range(self.numNodes):
            if i in partialSolution:
                self.prunes += 1
            else:
                partialSolution.append(i)  
                lastVertex = partialSolution[-2] if len(partialSolution) > 1 else partialSolution[-1]
                # print(f"Partial Solution apos adicionar {i}: {partialSolution}")
                # print(f"lastVertex: {lastVertex}")
                newCost = costPartialSolution + self.graph[lastVertex, i]  
                # print(f"newCost: {newCost}")
                bound = self.bound(partialSolution, newCost,)
                    
                if bound < self.bestCost:
                    self.brandAndBound(partialSolution, newCost)
                else:
                    self.prunes += 1
                    
                partialSolution.pop()       
        
    def solve(self, problem_path):
        # problem = self.problemManager.ReadProblem(problem_path)

        self.brandAndBound([], 0)  
        
        self.solution.append(self.solution[0])
        print(f"partial solutions: {self.iter}")

        return self.solution, self.bestCost, self.prunes
    
def main():
    graph = np.array([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ], dtype=float) 

    Solve = BranchAndBound(graph, 4)

    bestSolution, bestCost, prunes = Solve.solve(0)
    print(f"O melhor caminho é: {bestSolution}")
    print(f"O melhor custo é: {bestCost}")
    print(f"Número de podas feitas: {prunes}")


if __name__ == "__main__":
    main()
