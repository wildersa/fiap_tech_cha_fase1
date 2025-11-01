"""
Serviço para manipulação de dados de livros a partir de um arquivo CSV.
### Funções para carregar dados brutos e normalizar os dados do CSV
"""

from pathlib import Path
import csv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV = PROJECT_ROOT / "data" / "livros.csv"

#print(DEFAULT_CSV)

#df_csv = pd.read_csv(DEFAULT_CSV)

# Normalização
RATING_MAP = {"One":1,"Two":2,"Three":3,"Four":4,"Five":5}

def normalizar_rating(rating: str) -> int:
    return RATING_MAP.get(rating, 0)

def normalizar_preco(preco: str) -> float:
    try:
        preco = preco.replace(",", ".")
        preco = float(preco.replace("£", ""))
        return preco
    except ValueError:
        return 0.0

# Ler o CSV e imprimir o conteúdo
def carregar_livros_raw(df_path: Path = DEFAULT_CSV):
    """Lê o CSV e retorna uma lista de dicionários."""
    try:
        registros = []
        # Abre o arquivo
        with open(df_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                registros.append(row)
        return registros
    except Exception as e:
        print(f"Erro ao carregar o arquivo CSV: {e}")
        return []

def carregar_livros_normalizados(df_path: Path = DEFAULT_CSV):
    registros = carregar_livros_raw(df_path)
    for registro in registros:
        registro['rating'] = normalizar_rating(registro.get('rating', ''))
        registro['preco'] = normalizar_preco(registro.get('preco', '0'))
    return registros

if __name__ == "__main__":
    livros = carregar_livros_raw()
    print(livros)
    livros_norm = carregar_livros_normalizados()
    print(livros_norm)
