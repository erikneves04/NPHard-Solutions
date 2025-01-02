import numpy as np

class ProblemManager:
    __default_problem_path = 'Files/Problems'

    def ReadProblem(self, problem):
        """
        Lê os dados de um TSP com função de distância 2D e retorna uma matriz de adjacências.

        Parameters:
            problem (str): Nome do problema (sem extensão).

        Returns:
            np.ndarray: Matriz de adjacências com as distâncias entre os nós.
        """

        path = f"{self.__default_problem_path}/{problem}.tsp"
        try:
            with open(path, 'r') as file:
                lines = file.readlines()
            
            edge_weight_type = None
            node_coords = []
            
            for line in lines:
                line = line.strip()
                if line.startswith("EDGE_WEIGHT_TYPE"):
                    edge_weight_type = line.split(":")[1].strip()
                elif line.startswith("NODE_COORD_SECTION"):
                    break
            
            if edge_weight_type != "EUC_2D":
                raise ValueError(f"Unsupported EDGE_WEIGHT_TYPE: {edge_weight_type}")
            
            node_section_start = lines.index("NODE_COORD_SECTION\n") + 1
            for line in lines[node_section_start:]:
                if line.strip() == "EOF":
                    break
                parts = line.split()
                if len(parts) == 3:
                    _, x, y = parts
                    node_coords.append((float(x), float(y)))
            
            num_nodes = len(node_coords)
            adjacency_matrix = np.zeros((num_nodes, num_nodes))
            
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if i != j:
                        dist = np.sqrt((node_coords[i][0] - node_coords[j][0])**2 +
                                       (node_coords[i][1] - node_coords[j][1])**2)
                        adjacency_matrix[i, j] = dist
            
            return adjacency_matrix

        except FileNotFoundError:
            raise FileNotFoundError(f"Problem file not found: {path}")
        except Exception as e:
            raise RuntimeError(f"Error reading problem file {path}: {e}")