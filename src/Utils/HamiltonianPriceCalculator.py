class HamiltonianPriceCalculator:
    @staticmethod
    def Calculate(graph, path):
        total = 0
    
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            
            total += graph[u][v]
        
        return total
