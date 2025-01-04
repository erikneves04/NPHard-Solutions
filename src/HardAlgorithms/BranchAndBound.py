import numpy as np
import math

BESTCOST = float('inf')

class BranchAndBound:
    def __init__(self):
        self.graph = None
        self.numNodes = 0
        self.solution = None
        self.cost = BESTCOST     
        self.prunes = 0
        
    def bound(self, partialSolution):
        listMinCosts = []
        usedCostsCount = [0] * self.numNodes  

        for idx in range(len(partialSolution)):
            current = partialSolution[idx]
            prev = partialSolution[idx - 1] if idx > 0 else None
            next_ = partialSolution[idx + 1] if idx + 1 < len(partialSolution) else None

            if prev is not None:
                costPrev = float(self.graph[current, prev])
                listMinCosts.append(costPrev)
                usedCostsCount[current] += 1
            if next_ is not None:
                costNext = float(self.graph[current, next_])
                listMinCosts.append(costNext)
                usedCostsCount[current] += 1

        for i in range(self.numNodes):
            if usedCostsCount[i] >= 2: 
                continue

            self.graph[i, i] = BESTCOST

            validCosts = [float(cost) for cost in self.graph[i, :] if usedCostsCount[i] == 0 or cost not in usedCostsCount]
            if not validCosts:
                continue

            if usedCostsCount[i] == 1:
                minCost = np.partition(validCosts, 0)[0]
            else:
                minCost = np.partition(validCosts, 1)[:2]

            if isinstance(minCost, np.ndarray):
                for _ in minCost:
                    usedCostsCount[i] += 1  
                sumCosts = float(np.sum(minCost))
            else:
                usedCostsCount[i] += 1
                sumCosts = float(minCost)
                
            listMinCosts.append(sumCosts)

        bound = math.ceil(np.sum(listMinCosts) / 2)
        return bound

        
    def brandAndBound(self, partialSolution, costPartialSolution):
        startVertex = partialSolution[0]            
        for i in range(self.numNodes):
            if i in partialSolution:
                continue
            else:
                if len(partialSolution) + 1 == self.numNodes:
                    partialSolution.append(i)
                    endVertex = partialSolution[-1]
                    lastVertex = partialSolution[-2]
                    totalCost = costPartialSolution + self.graph[lastVertex,endVertex] + self.graph[endVertex, startVertex]
                    if totalCost < self.cost:
                        self.cost = totalCost
                        self.solution = partialSolution[:]
                    else:
                        self.prunes += 1
                    partialSolution.pop()
                    return                    
                else:   
                    partialSolution.append(i)  
                    lastVertex = partialSolution[-2] if len(partialSolution) > 1 else partialSolution[-1]
                    newCost = costPartialSolution + self.graph[lastVertex, i]
                    bound = self.bound(partialSolution)
                        
                    if bound < self.cost:
                        self.brandAndBound(partialSolution, newCost)
                    else:
                        self.prunes += 1
                        
                    partialSolution.pop()

    def solve(self, graph):
        """
        Resolve o problema de TSP utilizando o algoritmo Branch and Bound.

        :param graph: Grafo com os dados do problema.
        """
        self.graph = graph
        self.numNodes =  len(graph)
        self.brandAndBound([0], 0)

        self.solution.append(self.solution[0])
        #print(f"O melhor caminho é: {self.solution}")
        #print(f"O custo do caminho anterior é: {self.cost}")
        #print(f"O número de podas feitas foi: {self.prunes}")

        # TODO: retornar os valores correspondentes ÓTIMO, ESPAÇO_NECESSÁRIO
        return self.solution, 0
        