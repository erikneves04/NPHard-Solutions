from ProblemManager.ProblemManager import ProblemManager
import numpy as np
import math

BESTCOST = float('inf')

class BranchAndBound:
    def __init__(self, graph, numNodes):
        self.problemManager = ProblemManager()
        self.graph = graph
        self.numNodes = numNodes
        self.solution = None
        self.bestCost = BESTCOST     
        self.prunes = 0
        
    def bound(self, partialSolution):      
        listMinCosts = []
        usedCosts = {v: set() for v in range(self.numNodes)}

        print(f"\n[DEBUG] Calculando o limite (bound) para a solução parcial: {self.convert_indices_to_labels(partialSolution)}")

        for idx in range(len(partialSolution)):
            current = partialSolution[idx]
            prev = partialSolution[idx - 1] if idx > 0 else None
            next_ = partialSolution[idx + 1] if idx + 1 < len(partialSolution) else None

            if prev is not None:
                costPrev = float(self.graph[current, prev])  
                listMinCosts.append(costPrev)
                usedCosts[current].add(costPrev)
                print(f"[DEBUG] Custo de {self.convert_indices_to_labels([prev])} para {self.convert_indices_to_labels([current])}: {costPrev}")
            if next_ is not None:
                costNext = float(self.graph[current, next_]) 
                listMinCosts.append(costNext)
                usedCosts[current].add(costNext)
                print(f"[DEBUG] Custo de {self.convert_indices_to_labels([current])} para {self.convert_indices_to_labels([next_])}: {costNext}")

        print(f"[DEBUG] Lista de custos mínimos até agora: {listMinCosts}")
        print(f"[DEBUG] Custos utilizados: {usedCosts}")

        for i in range(self.numNodes):
            if len(usedCosts[i]) >= 2:
                print(f"[DEBUG] O nó {self.convert_indices_to_labels([i])} já tem pelo menos dois custos utilizados. Pulando.")
                continue  

            row = self.graph[i, :]  
            row[i] = BESTCOST 

            validCosts = [float(cost) for cost in row if cost not in usedCosts[i]]
            if not validCosts:
                print(f"[DEBUG] O nó {self.convert_indices_to_labels([i])} não tem custos válidos restantes. Pulando.")
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

            print(f"[DEBUG] Adicionando custo(s) mínimo(s) para o nó {self.convert_indices_to_labels([i])}: {minCost}")
            listMinCosts.append(sumCosts)

        bound = math.ceil(np.sum(listMinCosts) / 2)
        print(f"[DEBUG] Limite (bound) calculado: {bound}")
        return bound
        
    def brandAndBound(self, partialSolution, costPartialSolution):
        print(f"\n[DEBUG] Explorando a solução parcial: {self.convert_indices_to_labels(partialSolution)}")
        startVertex = partialSolution[0]            
        for i in range(self.numNodes):
            if i in partialSolution:
                continue
            else:
                if len(partialSolution) + 1 == self.numNodes:
                    partialSolution.append(i)
                    print(f"\n[DEBUG] Explorando a solução completa: {self.convert_indices_to_labels(partialSolution)}")
                    endVertex = partialSolution[-1]
                    lastVertex = partialSolution[-2]
                    totalCost = costPartialSolution + self.graph[lastVertex,endVertex] + self.graph[endVertex, startVertex]
                    if totalCost < self.bestCost:
                        self.bestCost = totalCost
                        self.solution = partialSolution[:]
                        print(f"[DEBUG] Nova melhor solução encontrada: {self.convert_indices_to_labels(self.solution)} com custo: {self.bestCost}")
                    else:
                        print("[DEBUG] Podada - Não foi encontrada uma solução melhor.")
                        self.prunes += 1
                        print(self.prunes)
                    partialSolution.pop()
                    return                    
                else:   
                    partialSolution.append(i)  
                    lastVertex = partialSolution[-2] if len(partialSolution) > 1 else partialSolution[-1]
                    newCost = costPartialSolution + self.graph[lastVertex, i]
                    print(f"[DEBUG] Adicionando o vértice {self.convert_indices_to_labels([i])} à solução.")
                    print(f"[DEBUG] Novo custo parcial: {newCost}")
                    bound = self.bound(partialSolution)
                        
                    if bound < self.bestCost:
                        print(f"[DEBUG] Limite {bound} é menor que o melhor custo {self.bestCost}. Explorando mais.")
                        self.brandAndBound(partialSolution, newCost)
                    else:
                        print(f"[DEBUG] Podada - Limite {bound} excede o melhor custo {self.bestCost}.")
                        self.prunes += 1
                        print(self.prunes)
                        
                    partialSolution.pop()

    def solve(self, problem_path):
        self.brandAndBound([0], 0)  
        self.solution.append(self.solution[0])
        return self.convert_indices_to_labels(self.solution), self.bestCost, self.prunes

    def convert_indices_to_labels(self, solution):
        labels = ['a', 'b', 'c', 'd', 'e']
        return [labels[i] for i in solution]

def main():
    graph = np.array([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ], dtype=float) 

    Solve = BranchAndBound(graph, 4)

    bestSolution, bestCost, prunes = Solve.solve(0)
    print(f"\nO melhor caminho é: {bestSolution}")
    print(f"O melhor custo é: {bestCost}")
    print(f"Número de podas feitas: {prunes}")

if __name__ == "__main__":
    main()
