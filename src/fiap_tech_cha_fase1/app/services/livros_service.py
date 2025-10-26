"""
Serviço para manipulação de dados de livros a partir de um arquivo CSV.

### Funções pra dar suporte aos endpoints obrigatórios da API

- `GET /api/v1/books` — lista todos os livros;
- `GET /api/v1/books/{id}` — detalhes de um livro pelo ID;
- `GET /api/v1/books/search?title={title}&category={category}` — busca por título e/ou categoria;
- `GET /api/v1/categories` — lista todas as categorias;

"""

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV = PROJECT_ROOT / "data" / "livros.csv"

print(DEFAULT_CSV)

# Ler o CSV e imprimir o conteúdo usando encodfing utf-8
def carregar_livros():
    try:
        with DEFAULT_CSV.open(newline="", encoding="utf-8") as csvfile:
            leitor = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            return [linha for linha in leitor]
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {DEFAULT_CSV}")
        return []
    except csv.Error as e:
        print(f"Erro ao ler CSV: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return []

def listar_livros():
    return carregar_livros()

def obter_livro_por_id(livro_id: str):
    for livro in carregar_livros():
        if livro['id'] == livro_id:
            return livro
    return None

def buscar_livros(titulo: str = None, categoria: str = None):
    """Filtra livros por título e/ou categoria (case-insensitive).
    Args: titulo: parte do título; categoria: nome exato da categoria.
    Returns: lista de registros do CSV já filtrados.
    """
    dados = carregar_livros()
    if titulo:
        t = titulo.strip().lower()
        dados = [l for l in dados if t in l.get("titulo", "").lower()]
    if categoria:
        c = categoria.strip().lower()
        dados = [l for l in dados if l.get("categoria", "").lower() == c]

    return dados

def listar_categorias():
    categorias = []
    for livro in carregar_livros():
        categorias.append(livro['categoria'])
    return sorted(set(categorias))

if __name__ == "__main__":
    # Testando as funções
    print(f'\nObter categorias: \n{listar_categorias()}\n')
    print(f'Obter livro por ID ("a22124811bfa8350"): \n{obter_livro_por_id("a22124811bfa8350")}\n')
    print(f'Buscar livros (titulo="A Year in Provence (Provence #1)"): \n{buscar_livros(titulo="A Year in Provence (Provence #1)")}\n')
    print(f'Buscar livros (categoria="Travel"): \n{buscar_livros(categoria="Travel")}\n')