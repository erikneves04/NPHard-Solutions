import heapq
import numpy as np
import math

BESTCOST = float('inf')

class BranchAndBound:
    """
    Classe que implementa o algoritmo Branch and Bound para resolver o problema do Caixeiro Viajante (TSP).
    """
    def __init__(self):
        """
        Inicializa a classe com um grafo vazio, custo de solução infinito,
        vetor de soluções vazio, e 0 podas.
        """
        self.graph = None
        self.numNodes = 0
        self.solution = None
        self.cost = BESTCOST     
        self.prunes = 0
        
    def __bound(self, partialSolution):
        """
        Calcula o bound para uma solução parcial.

        :param partialSolution: Vetor representando a solução parcial (sequência de nós).
        :return: Valor do bound estimado para a solução parcial.
        """        
        listMinCosts = []
        usedEdges = []  
        usedCostsCount = [0] * self.numNodes

        for idx in range(len(partialSolution)):
            current = partialSolution[idx]
            prev = partialSolution[idx - 1] if idx > 0 else None
            next_ = partialSolution[idx + 1] if idx + 1 < len(partialSolution) else None

            if prev is not None:
                costPrev = float(self.graph[current, prev])
                listMinCosts.append(costPrev)
                usedEdges.append([current, prev])
                usedCostsCount[current] += 1

            if next_ is not None:
                costNext = float(self.graph[current, next_])
                listMinCosts.append(costNext)
                usedEdges.append([current, next_])
                usedCostsCount[current] += 1

        for i in range(self.numNodes):
            if usedCostsCount[i] >= 2:
                continue
            
            self.graph[i, i] = BESTCOST

            if usedCostsCount[i] == 1:
                validCosts = [float(self.graph[i, j]) for j in range(self.numNodes) if [i, j] not in usedEdges and i != j]
                minCost = min(validCosts)  
                listMinCosts.append(minCost)
            else:
                validCosts = [float(self.graph[i, j]) for j in range(self.numNodes) if [i, j] not in usedEdges and i != j]
                minCosts = sorted(validCosts)[:2]  
                listMinCosts.extend(minCosts)  
                
        bound = math.ceil(np.sum(listMinCosts) / 2)        
        return bound
    
    def __brand_and_bound(self, partialSolution, costPartialSolution):
        """
        Branch and Bound para encontrar a solução ótima.

        :param partialSolution: Lista representando a solução parcial inicial.
        :param costPartialSolution: Custo da solução parcial inicial.
        """
        startVertex = partialSolution[0]
        
        queue = []
        initialBound = self.__bound(partialSolution)
        heapq.heappush(queue, (initialBound, partialSolution, costPartialSolution))  
        
        while queue:
            currentBound, currentSolution, currentCost = heapq.heappop(queue)            
            if len(currentSolution) == self.numNodes:
                totalCost = currentCost + self.graph[currentSolution[-1], startVertex]                
                if totalCost < self.cost:
                    self.cost = totalCost
                    self.solution = currentSolution[:]
                else:
                    self.prunes += 1
                continue
            
            if len(currentSolution) == self.numNodes - 1:
                for i in range(self.numNodes):
                    if i not in currentSolution:
                        totalCost = currentCost + self.graph[currentSolution[-1], i] + self.graph[i, startVertex]
                        if totalCost < self.cost:
                            self.cost = totalCost
                            self.solution = currentSolution + [i, startVertex]
                        else:
                            self.prunes += 1
                continue
                        
            
            for i in range(self.numNodes):
                if i in currentSolution:
                    continue
                print(currentSolution)
                newSolution = currentSolution + [i]
                newCost = currentCost + self.graph[currentSolution[-1], i]
                
                bound = self.__bound(newSolution)
                
                if bound < self.cost:
                    heapq.heappush(queue, (bound, newSolution, newCost))
                else:
                    self.prunes += 1
                    
    def __estimate_space_required__(self, graph):
        """
        Calcula uma estimativa do espaço necessário gasto para resolver
        a instância atual do problema

        :param graph: Grafo com os dados do problema.
        :return total_space: Espaço estimado total gasto.
        """
        num_nodes = len(graph)
                
        # Aproximações do espaço (em bytes):
        space_per_node = 8 
        
        # Aproximação do espaço gasto por todas as soluções parciais
        total_space_partials_solutions = num_nodes**2 * space_per_node  
        
        # Espaço total (em bytes)
        total_space = (
            total_space_partials_solutions +
            num_nodes * space_per_node 
        )
        return total_space

    def solve(self, graph):
        """
        Resolve o problema de TSP utilizando o algoritmo Branch and Bound.

        :param graph: Grafo com os dados do problema.
        :return solution: Solução ótima para o problema.
        :retunr space_required: Espaço total gasto nessa instância.
        """
        self.graph = graph
        self.numNodes =  len(graph)
        self.__brand_and_bound([0], 0)
        
        space_required = self.__estimate_space_required__(graph)
        
        return self.solution, space_required
        