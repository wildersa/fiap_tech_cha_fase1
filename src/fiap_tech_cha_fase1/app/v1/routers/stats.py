"""
Roteador FastAPI para endpoints relacionados a overview.

### Endpoints opicionais da API
- `GET /api/v1/stats/overview` — estatísticas gerais (total de livros, preço médio, distribuição de ratings);
- `GET /api/v1/stats/categories` — estatísticas por categoria (quantidade, preços);
"""

from fastapi import APIRouter, HTTPException
from fiap_tech_cha_fase1.app.services.stats_service import computar_estatisticas_overview, computar_estatisticas_por_categoria
from fiap_tech_cha_fase1.app.services.dataset_service import carregar_livros_normalizados

router = APIRouter(prefix ="/api/v1/stats", tags=["stats"])

@router.get("/overview", summary="Estatísticas gerais dos livros",
            description="Retorna estatísticas gerais, como total de livros, preço médio e distribuição de ratings.")
async def estatisticas_gerais():
    try:
        livros = carregar_livros_normalizados()
        return computar_estatisticas_overview(livros)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao computar estatísticas: {e}")

@router.get("/categories", summary="Estatísticas por categoria",
            description="Retorna estatísticas por categoria, como quantidade de livros e preços médios.")
async def estatisticas_por_categoria():
    try:
        livros = carregar_livros_normalizados()
        return computar_estatisticas_por_categoria(livros)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao computar estatísticas: {e}")
