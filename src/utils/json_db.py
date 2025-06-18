import json #módulo padrão da biblioteca, python -> json: conversão, leitura e escrita
from pathlib import Path

DB_PATH = Path("data/pessoas.json") #caminho até o banco de dados

#dicionários são compostos por chaves que são "nome", "IDM", etc

def carregar_dados():
    if DB_PATH.exists(): #lê o bando de dados JSON e retorna como lista de dicionários
        with open(DB_PATH, 'r', encoding='utf-8') as arquivo: #with abre o arquivo, encoding = 'utf-8 garante caracteres especiais
            try:
                return json.load(arquivo) #lê o arquivo e converte em estrutura python -> lista de dicionários. se bem sucedido retorna dados
            except json.JSONDecodeError: # caso de erros
                return []  # Retorna lista vazia se o JSON estiver vazio
    return []

def salvar_dados(dados): #grava os dados recebidos em lista de dicionário e att o banco
    with open(DB_PATH, 'w', encoding='utf-8') as arquivo: # 'w' = subescreve no arquivo.
        json.dump(dados, arquivo, indent=4, ensure_ascii=False) 
