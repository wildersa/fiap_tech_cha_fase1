"""
Serviço para manipulação de dados de livros a partir de um arquivo CSV.

### Funções pra dar suporte aos endpoints obrigatórios da API

- `GET /api/v1/books` — lista todos os livros;
- `GET /api/v1/books/{id}` — detalhes de um livro pelo ID;
- `GET /api/v1/books/search?title={title}&category={category}` — busca por título e/ou categoria;
- `GET /api/v1/categories` — lista todas as categorias;

### Funções pra dar suporte aos endpoints opcionais da API

- `GET /api/v1/books/top-rated` — livros com melhor rating;
- `GET /api/v1/books/price-range?min={min}&max={max}` — filtrar por faixa de preço.

"""

from .dataset_service import carregar_livros_raw, carregar_livros_normalizados

def listar_livros():
    return carregar_livros_raw()

def obter_livro_por_id(livro_id: str):
    for livro in carregar_livros_raw():
        if livro['id'] == livro_id:
            return livro
    return None

def buscar_livros(titulo: str = None, categoria: str = None):
    """Filtra livros por título e/ou categoria (case-insensitive).
    Args: titulo: parte do título; categoria: nome exato da categoria.
    Returns: lista de registros do CSV já filtrados.
    """
    dados = carregar_livros_raw()
    if titulo:
        t = titulo.strip().lower()
        dados = [l for l in dados if t in l.get("titulo", "").lower()]
    if categoria:
        c = categoria.strip().lower()
        dados = [l for l in dados if l.get("categoria", "").lower() == c]
    return dados

def listar_categorias():
    categorias = []
    for livro in carregar_livros_raw():
        categorias.append(livro['categoria'])
    return sorted(set(categorias))

def listar_livros_top_rated(top_n: int = 10):
    livros = carregar_livros_normalizados()
    livros_ordenados = sorted(livros, key=lambda x: (x['rating'], x['preco']), reverse=True)
    return livros_ordenados[:top_n]

def filtrar_livros_por_faixa_de_preco(preco_min: float = None, preco_max: float = None):
    livros = carregar_livros_normalizados()
    livros = [l for l in livros if l['preco'] >= preco_min]
    livros = [l for l in livros if l['preco'] <= preco_max]
    return sorted(livros, key=lambda x: x['preco'], reverse=False)