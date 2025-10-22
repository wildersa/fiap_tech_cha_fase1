"""
### Endpoints obrigatórios da API

- `GET /api/v1/books` — lista todos os livros;
- `GET /api/v1/books/{id}` — detalhes de um livro pelo ID;
- `GET /api/v1/books/search?title={title}&category={category}` — busca por título e/ou categoria;
- `GET /api/v1/categories` — lista todas as categorias;
- `GET /api/v1/health` — status da API.
"""

from fastapi import APIRouter, Query, HTTPException
from fiap_tech_cha_fase1.app.v1.schemas import LivroBase
from fiap_tech_cha_fase1.app.services.livros_service import (
    listar_livros,
    obter_livro_por_id,
    buscar_livros,
    listar_categorias
)

router = APIRouter()

@router.get("/api/v1/books", response_model=list[LivroBase])
async def lista():
    try:
        rows = listar_livros()
        return [LivroBase.model_validate(r) for r in rows]
    except Exception as e:
        # captura erros genéricos e retorna resposta HTTP controlada
        raise HTTPException(status_code=500, detail=f"Erro ao listar livros: {e}")

@router.get("/api/v1/books/search", summary="Busca por título e/ou categoria")
async def busca_livros(title: str = Query(None), category: str = Query(None)):
    try:
        resultados = buscar_livros(titulo=title, categoria=category)
        return [LivroBase.model_validate(r) for r in resultados]
    except Exception as e:
        # captura erros genéricos e retorna resposta HTTP controlada
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livros: {e}")

@router.get("/api/v1/books/{id}", summary="Detalhes de um livro pelo ID")
async def detalhes_livro(id: str):
    livro = obter_livro_por_id(id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return LivroBase.model_validate(livro)


@router.get("/api/v1/categories", summary="Lista todas as categorias")
async def lista_categorias():
    try:
        categorias = listar_categorias()
        return categorias
    except Exception as e:
        # captura erros genéricos e retorna resposta HTTP controlada
        raise HTTPException(status_code=500, detail=f"Erro ao listar categorias: {e}")
