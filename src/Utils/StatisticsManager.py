import pandas as pd
import json
import os

class StatisticsManager:
    """
    Gerencia e registra dados estatísticos do desempenho de algoritmos, comparando soluções com valores ótimos.

    Atributos:
        __default_result_directory (str): Diretório onde os resultados serão salvos.
        __optimal_soltions_path (str): Caminho para o arquivo JSON com as soluções ótimas conhecidas.
        __dataframe (pd.DataFrame): Armazena temporariamente as estatísticas de execução.
        __aggregated_file_path (str): Caminho para salvar o arquivo CSV com os resultados agregados.
        __optimal_solutions (dict): Soluções ótimas carregadas para instâncias do problema.
    """

    __default_result_directory = 'Results'
    __optimal_soltions_path = 'Files/Optimal-Solutions.json'

    def __init__(self, aggregated_file_name):
        """
        Inicializa o `StatisticsManager` com um nome de arquivo específico para agregação.

        Args:
            aggregated_file_name (str): Nome do arquivo onde os resultados serão agregados.
        """
        self.__dataframe = pd.DataFrame(columns=[
            'problem', 'algorithm', 'time-required', 'space-required',
            'solution', 'optimal-solution', 'solution-quality', 'problem-size'
        ])
        self.__aggregated_file_path = os.path.join(
            self.__default_result_directory, f'{aggregated_file_name}.csv'
        )

        with open(self.__optimal_soltions_path, 'r') as file:
            self.__optimal_solutions = json.load(file)

    def Save(self):
        """
        Salva o DataFrame atual em um arquivo CSV, adicionando dados se o arquivo já existir.
        Cria o diretório se ele ainda não existir.
        """
        if not os.path.exists(self.__default_result_directory):
            os.makedirs(self.__default_result_directory)

        if len(self.__dataframe) == 0:
            return

        if os.path.exists(self.__aggregated_file_path):
            existing_data = pd.read_csv(self.__aggregated_file_path)
            combined_data = pd.concat([existing_data, self.__dataframe], ignore_index=True)
        else:
            combined_data = self.__dataframe

        combined_data.to_csv(self.__aggregated_file_path, index=False)

    def __compare_solutions__(self, problem, solution):
        """
        Compara a solução obtida com a solução ótima para um problema.

        Args:
            problem (str): Identificador da instância do problema.
            solution (float): Solução obtida pelo algoritmo.

        Returns:
            tuple: Um par (optimal_value, quality), onde:
                - optimal_value (float): Valor da solução ótima para o problema.
                - quality (float): Qualidade relativa da solução obtida.
        """
        optimal_value = self.__optimal_solutions.get(problem)
        quality = abs(optimal_value - solution) / max(optimal_value, solution)
        return optimal_value, quality

    def __add_dataframe_row__(self, problem, solution, algorithm, time_required, 
                              space_required, optimal_solution, solution_quality, graph_size):
        """
        Adiciona uma nova linha de dados de execução ao DataFrame.

        Args:
            problem (str): Identificador da instância do problema.
            solution (float): Solução obtida pelo algoritmo.
            algorithm (str): Nome do algoritmo utilizado.
            time_required (float): Tempo gasto para encontrar a solução, em segundos.
            space_required (float): Espaço utilizado pelo algoritmo, em bytes.
            optimal_solution (float): Valor da solução ótima para o problema.
            solution_quality (float): Qualidade relativa da solução obtida.
            graph_size (int): Tamanho do grafo do problema.
        """
        new_row = {
            'problem': problem,
            'algorithm': algorithm,
            'time-required': time_required,
            'space-required': space_required,
            'solution': solution,
            'optimal-solution': optimal_solution,
            'solution-quality': solution_quality,
            'problem-size': graph_size
        }
        self.__dataframe.loc[len(self.__dataframe)] = new_row

    def AddTimeoutSolution(self, problem, algorithm, time_required, graph_size):
        """
        Registra uma execução onde o algoritmo excedeu o limite de tempo.

        Args:
            problem (str): Identificador da instância do problema.
            algorithm (str): Nome do algoritmo utilizado.
            time_required (float): Tempo total decorrido, em segundos.
            graph_size (int): Tamanho do grafo do problema.
        """
        optimal_value = self.__optimal_solutions.get(problem)
        self.__add_dataframe_row__(problem, None, algorithm, time_required, None, optimal_value, None, graph_size)

    def AddSolution(self, problem, solution, algorithm, time_required, space_required, graph_size):
        """
        Registra uma solução bem-sucedida, comparando-a com a solução ótima.

        Args:
            problem (str): Identificador da instância do problema.
            solution (float): Solução obtida pelo algoritmo.
            algorithm (str): Nome do algoritmo utilizado.
            time_required (float): Tempo gasto para encontrar a solução, em segundos.
            space_required (float): Espaço utilizado pelo algoritmo, em bytes.
            graph_size (int): Tamanho do grafo do problema.
        """
        optimal, quality = self.__compare_solutions__(problem, solution)
        self.__add_dataframe_row__(problem, solution, algorithm, time_required, space_required, optimal, quality, graph_size)