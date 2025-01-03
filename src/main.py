import argparse
import signal
import time
from enum import Enum

from HardAlgorithms.BranchAndBound import BranchAndBound
from HardAlgorithms.Christofides import Christofides
from HardAlgorithms.TwiceAroundTheTree import TwiceAroundTheTree
from Utils.StatisticsManager import StatisticsManager

# Constantes
DEFAULT_TIME_LIMITATION = 30
DEFAULT_STATISTICS_FILE_NAME = 'data'

# Serviço de gerenciamento de estatísticas
STATISTICS_SERVICE = None # Inicializado no main

class Algorithms(Enum):
    """
    Enumeração de algoritmos disponíveis.

    BRANCHANDBOUND: Algoritmo de branch and bound.
    CHRISTOFIDES: Algoritmo de Christofides.
    TWICEAROUNDTHETREE: Algoritmo de twice around the tree.
    ALL: Executa os três algoritmos.
    """
    BRANCHANDBOUND = "branch-and-bound"
    CHRISTOFIDES = "christofides"
    TWICEAROUNDTHETREE = "twice-around-the-tree"
    ALL = 'all'

    def __str__(self):
        return self.value

def parseArgs():
    """
    Função para fazer o parsing dos argumentos da linha de comando.

    :return: Retorna um objeto com os argumentos parseados.
    """
    parser = argparse.ArgumentParser(description="Aplicação para solução de problemas NP-Dificeis")

    parser.add_argument('--max-minutes', type=int, required=False, default=DEFAULT_TIME_LIMITATION, help='Número máximo de minutos para essa execução.')
    parser.add_argument('--problem', type=str, required=True, help='Identificação do arquivo de entrada com o problema.')
    parser.add_argument('--algorithm', type=Algorithms, choices=list(Algorithms), required=True, help='Seleção do algoritmo que será usado para resolver o problema.')
    parser.add_argument('--statistics-file-name', type=str, required=False, default=DEFAULT_STATISTICS_FILE_NAME, help='Nome do arquivo (sem extensão) com as estatísticas coletadas.')

    return parser.parse_args() 

def ExecuteWithTimeout(algorithm_func, problem, time_limit, algorithm_identification):
    """
    Executa a função do algoritmo com limite de tempo.

    :param algorithm_func: Função do algoritmo a ser executada.
    :param problem: Identificação do arquivo do problema.
    :param time_limit: Tempo limite em minutos.
    :param algorithm_identification: Enumerador de identificação do algoritmo.
    """

    def TimeoutHandler(signum, frame):
        raise TimeoutError(f"Execution exceeded the time limit of {time_limit} minutes.")

    global STATISTICS_SERVICE
    STATISTICS_SERVICE

    signal.signal(signal.SIGALRM, TimeoutHandler)
    signal.alarm(time_limit * 60)

    try:
        start_time = time.time()
        solution, space_required = algorithm_func(problem)
        time_required = time.time() - start_time
        
        STATISTICS_SERVICE.AddSolution(problem, solution, str(algorithm_identification), time_required, space_required)
    except TimeoutError as e:
        print(e)
        STATISTICS_SERVICE.AddTimeoutSolution(problem, str(algorithm_identification), time_limit * 60)
    finally:
        signal.alarm(0)

def main():
    """
    Função principal do programa. Resolve o problema especificado com base no algoritmo selecionado nos parâmetros de entrada respeitando a limitação de tempo imposta.
    """
    args = parseArgs()

    # Inicialização do serviço de gerenciamento de estatísticas
    global STATISTICS_SERVICE
    STATISTICS_SERVICE = StatisticsManager(args.statistics_file_name)

    algorithm_option = args.algorithm
    if algorithm_option == Algorithms.ALL:
        ExecuteWithTimeout(BranchAndBound().solve, args.problem, args.max_minutes, Algorithms.BRANCHANDBOUND)
        ExecuteWithTimeout(Christofides().solve, args.problem, args.max_minutes, Algorithms.CHRISTOFIDES)
        ExecuteWithTimeout(TwiceAroundTheTree().solve, args.problem, args.max_minutes, Algorithms.TWICEAROUNDTHETREE)
    
    elif algorithm_option == Algorithms.BRANCHANDBOUND:
        ExecuteWithTimeout(BranchAndBound().solve, args.problem, args.max_minutes, Algorithms.BRANCHANDBOUND)
    elif algorithm_option == Algorithms.CHRISTOFIDES:
        ExecuteWithTimeout(Christofides().solve, args.problem, args.max_minutes, Algorithms.CHRISTOFIDES)
    elif algorithm_option == Algorithms.TWICEAROUNDTHETREE:
        ExecuteWithTimeout(TwiceAroundTheTree().solve, args.problem, args.max_minutes, Algorithms.TWICEAROUNDTHETREE)

    STATISTICS_SERVICE.Save()

if __name__ == "__main__":
    main()