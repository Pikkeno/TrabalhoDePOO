import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "desafios.json"

def carregar_dados():
    if DB_PATH.exists():
        with open(DB_PATH, "r", encoding="utf-8") as arquivo:
            try:
                return json.load(arquivo)
            except json.JSONDecodeError:
                return []
    return []

def salvar_dados(dados):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)