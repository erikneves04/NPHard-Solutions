#!/bin/bash

# Diretório com os problemas
directory="Files/Problems"

# Variáveis de ambiente
export MAX_MINUTES=30
export STATISTICS_FILE_NAME="SimulationV1-bnb-laboratory"
export ALGORITHM="branch-and-bound"

for file in "$directory"/*; do
    if [ -f "$file" ]; then
        filename=$(basename -- "$file")
        problem="${filename%.*}"  # Remove a extensão do arquivo

        # Executa o script Python e captura erros sem parar o loop
        echo "Executando o algoritmo $ALGORITHM para o problema $problem..."
        python3 src/main.py --problem "$problem" --algorithm "$ALGORITHM" --max-minutes "$MAX_MINUTES" --statistics-file-name "$STATISTICS_FILE_NAME"
        if [ $? -ne 0 ]; then
            echo "Erro ao executar para o problema $problem com o algoritmo $ALGORITHM. Continuando..."
        fi
    fi
done
