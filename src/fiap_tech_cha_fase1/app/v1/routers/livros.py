"""
Roteador FastAPI para endpoints relacionados a livros.

### Endpoints obrigatórios da API

- `GET /api/v1/books` — lista todos os livros;
- `GET /api/v1/books/{id}` — detalhes de um livro pelo ID;
- `GET /api/v1/books/search?title={title}&category={category}` — busca por título e/ou categoria;
- `GET /api/v1/categories` — lista todas as categorias;
- `GET /api/v1/health` — status da API.

### Endpoints opcionais da API
- `GET /api/v1/books/top-rated` — livros com melhor rating;
- `GET /api/v1/books/price-range?min={min}&max={max}` — filtrar por faixa de preço.

"""

from fastapi import APIRouter, Query, HTTPException
from fiap_tech_cha_fase1.app.v1.schemas import LivroBase, LivroBaseNormalizado
from fiap_tech_cha_fase1.app.services.livros_service import (
    listar_livros,
    obter_livro_por_id,
    buscar_livros,
    listar_categorias,
    listar_livros_top_rated,
    filtrar_livros_por_faixa_de_preco
)

router = APIRouter(prefix ="/api/v1", tags=["books"])

@router.get("/books", response_model=list[LivroBase], summary="Lista livros",
            description="Retorna todos os livros do CSV.")
async def lista():
    try:
        rows = listar_livros()
        return [LivroBase.model_validate(r) for r in rows]
    except Exception as e:
        # captura erros
        raise HTTPException(status_code=500, detail=f"Erro ao listar livros: {e}")

@router.get("/books/search", summary="Busca por título e/ou categoria",
             description="Filtra livros pelo título (parcial, case-insensitive) e/ou categoria (exata, case-insensitive).")
async def busca_livros(title: str = Query(None), category: str = Query(None)):
    try:
        resultados = buscar_livros(titulo=title, categoria=category)
        return [LivroBase.model_validate(r) for r in resultados]
    except Exception as e:
        # captura erros
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livros: {e}")

@router.get("/categories", summary="Lista todas as categorias",
             description="Retorna uma lista com todas as categorias de livros disponíveis.")
async def lista_categorias():
    try:
        categorias = listar_categorias()
        return categorias
    except Exception as e:
        # captura erros
        raise HTTPException(status_code=500, detail=f"Erro ao listar categorias: {e}")

@router.get("/books/top-rated", summary="Lista livros com melhor rating",
            description="Retorna os livros com melhor avaliação (rating).")
async def lista_livros_top_rated():
    try:
        livros = listar_livros_top_rated()
        return [LivroBaseNormalizado.model_validate(l) for l in livros]
    except Exception as e:
        # captura erros
        raise HTTPException(status_code=500, detail=f"Erro ao listar livros: {e}")

@router.get("/books/price-range", summary="Filtra livros por faixa de preço",
            description="Retorna os livros que estão dentro da faixa de preço especificada.")
async def filtra_livros_por_faixa_de_preco(min: float = Query(0.0), max: float = Query(5000.0)):
    try:
        livros = filtrar_livros_por_faixa_de_preco(preco_min=min, preco_max=max)
        return [LivroBaseNormalizado.model_validate(l) for l in livros]
    except Exception as e:
        # captura erros
        raise HTTPException(status_code=500, detail=f"Erro ao filtrar livros: {e}")

@router.get("/books/{id}", summary="Detalhes de um livro pelo ID",
            description="Retorna os detalhes completos de um livro específico pelo seu ID.")
async def detalhes_livro(id: str):
    livro = obter_livro_por_id(id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return LivroBase.model_validate(livro)