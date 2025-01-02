import argparse
import signal
from enum import Enum

from HardAlgorithms.BranchAndBound import BranchAndBound
from HardAlgorithms.Christofides import Christofides
from HardAlgorithms.TwiceAroundTheTree import TwiceAroundTheTree

# Constantes
DEFAULT_TIME_LIMITATION = 30

class Algorithms(Enum):
    """
    Enumeração de algoritmos disponíveis.

    BRANCHANDBOUND: Algoritmo de branch and bound.
    CHRISTOFIDES: Algoritmo de Christofides.
    TWICEAROUNDTHETREE: Algoritmo de twice around the tree.
    """
    BRANCHANDBOUND = "branch-and-bound"
    CHRISTOFIDES = "christofides"
    TWICEAROUNDTHETREE = "twice-around-the-tree"

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

    return parser.parse_args() 

def TimeoutHandler(signum, frame):
    """
    Manipulador de sinal para o tempo limite.

    :param signum: Sinal recebido.
    :param frame: Frame de execução atual.
    """
    raise TimeoutError("Tempo limite de execução excedido.")

def ExecuteWithTimeout(algorithm_func, problem, time_limit):
    """
    Executa a função do algoritmo com limite de tempo.

    :param algorithm_func: Função do algoritmo a ser executada.
    :param problem: Identificação do arquivo do problema.
    :param time_limit: Tempo limite em minutos.
    """
    signal.signal(signal.SIGALRM, TimeoutHandler)
    signal.alarm(time_limit * 60)

    try:
        algorithm_func(problem)
    except TimeoutError as e:
        print(e)
        # TODO: Tratar o erro de timeout (tempo limite de execução excedido)
    finally:
        signal.alarm(0)

def main():
    """
    Função principal do programa. Resolve o problema especificado com base no algoritmo selecionado nos parâmetros de entrada respeitando a limitação de tempo imposta.
    """
    args = parseArgs()

    algorithm_option = args.algorithm

    if algorithm_option == Algorithms.BRANCHANDBOUND:
        model = BranchAndBound()
        ExecuteWithTimeout(model.solve, args.problem, args.max_minutes)
    elif algorithm_option == Algorithms.CHRISTOFIDES:
        model = Christofides()
        ExecuteWithTimeout(model.solve, args.problem, args.max_minutes)
    elif algorithm_option == Algorithms.TWICEAROUNDTHETREE:
        model = TwiceAroundTheTree()
        ExecuteWithTimeout(model.solve, args.problem, args.max_minutes)

if __name__ == "__main__":
    main()