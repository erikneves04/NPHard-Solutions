# Resolução do Problema do Caixeiro Viajante (TSP) Euclidiano

Este projeto resolve instâncias do **Problema do Caixeiro Viajante (TSP)** euclidiano utilizando algoritmos exatos e heurísticos. O TSP consiste em encontrar o menor caminho que visita um conjunto de cidades exatamente uma vez e retorna à cidade inicial.

#### Integrantes:
- **Gabriel Campos Prudente**  
- **Erik Roberto Reis Neves**

## Sobre o TSP Euclidiano

O TSP Euclidiano utiliza a **distância euclidiana** (distância "em linha reta") entre pontos em um plano 2D. É um problema clássico de otimização amplamente estudado.

## Origem dos Dados

Os dados são provenientes da **TSPLIB**, um repositório padrão de instâncias do TSP e problemas relacionados. Este programa trabalha exclusivamente com instâncias 2D e métricas baseadas em distâncias euclidianas.

## Algoritmos Implementados

- **Branch-and-Bound**: Método exato para encontrar a solução ótima.
- **Christofides**: Heurística que gera uma solução próxima do ótimo.
- **Twice Around the Tree**: Heurística baseada em árvores geradoras mínimas.

## Como Executar

### Parâmetros Disponíveis

| Parâmetro                 | Descrição                                                                                       | Padrão             |
|---------------------------|-------------------------------------------------------------------------------------------------|--------------------|
| `--problem`               | Caminho para o arquivo contendo o problema (formato TSPLIB).                                    | **Obrigatório**    |
| `--algorithm`             | Algoritmo a ser usado: `branch-and-bound`, `christofides`, `twice-around-the-tree`, ou `all`.   | **Obrigatório**    |
| `--max-minutes`           | Limite de tempo (em minutos) para execução.                                                     | 30 minutos         |
| `--statistics-file-name`  | Nome do arquivo onde as estatísticas serão salvas (sem extensão).                               | `data`             |

Exemplo:
```bash
python main.py --problem tsp_instance.tsp --algorithm branch-and-bound --max-minutes 30
