#!/bin/bash

VENV_DIR="venv"

# Verifica se o ambiente virtual já existe
if [ -d "$VENV_DIR" ]; then
  echo "O ambiente virtual '$VENV_DIR' já existe. Ativando..."
else
  # Cria o ambiente virtual
  echo "Criando o ambiente virtual..."
  python3 -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate