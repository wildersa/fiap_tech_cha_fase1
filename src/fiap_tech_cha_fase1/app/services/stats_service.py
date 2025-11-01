"""
Serviço para computar estatísticas gerais dos livros.

### Função pra dar suporte ao endpoint opcional da API:

- `GET /api/v1/stats/overview` — estatísticas gerais (total de livros, preço médio, distribuição de ratings);
- `GET /api/v1/stats/categories` — estatísticas por categoria (quantidade, preços);

Usa o dataset_service para carregar os dados normalizados.
"""

def computar_estatisticas_overview(livros):
    """Computa estatísticas gerais dos livros.
    Args:
        livros: lista de registros do CSV em dataframe já normalizados.
    Returns:
        dicionário com as estatísticas computadas.
    """
    total_livros = len(livros)
    if total_livros == 0:
        return {
            "total_livros": 0,
            "preco_medio": 0.0,
            "distribuicao_ratings": {}
        }

    soma_precos = sum(livro['preco'] for livro in livros)
    preco_medio = soma_precos / total_livros

    distribuicao_ratings = {}
    for livro in livros:
        rating = livro['rating']
        distribuicao_ratings[rating] = distribuicao_ratings.get(rating, 0) + 1

    return {
        "total_livros": total_livros,
        "preco_medio": round(preco_medio, 2),
        "distribuicao_ratings": distribuicao_ratings
    }

def computar_estatisticas_por_categoria(livros):
    """Computa estatísticas por categoria dos livros.
    Args:
        livros: lista de registros do CSV em dataframe já normalizados.
    Returns:
        dicionário com as estatísticas por categoria.
    """
    estatisticas = {}
    for livro in livros:
        categoria = livro['categoria']
        if categoria not in estatisticas:
            estatisticas[categoria] = {
                "quantidade": 0,
                "soma_precos": 0.0
            }
        estatisticas[categoria]["quantidade"] += 1
        estatisticas[categoria]["soma_precos"] += livro['preco']

    # Calcular preço médio, min, max por categoria
    for categoria, stats in estatisticas.items():
        quantidade = stats["quantidade"]
        soma_precos = stats["soma_precos"]
        stats["preco_medio"] = round(soma_precos / quantidade, 2) if quantidade > 0 else 0.0
        stats["preco_min"] = round(min(livro['preco'] for livro in livros if livro['categoria'] == categoria), 2) if quantidade > 0 else 0.0
        stats["preco_max"] = round(max(livro['preco'] for livro in livros if livro['categoria'] == categoria), 2) if quantidade > 0 else 0.0
        del stats["soma_precos"]  # Remove soma_precos, não é necessário no resultado final

    return estatisticas