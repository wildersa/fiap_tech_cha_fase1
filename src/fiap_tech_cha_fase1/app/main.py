'''
### Endpoints Obrigatórios

- **GET /api/v1/books**: Lista todos os livros.
  - Response: Lista de objetos JSON com id, título, preço, etc.

- **GET /api/v1/books/{id}**: Detalhes de um livro específico.
  - Response: Objeto JSON completo do livro.

- **GET /api/v1/books/search?title={title}&category={category}**: Busca por título e/ou categoria.
  - Query params: title (string), category (string).
  - Response: Lista filtrada.

- **GET /api/v1/categories**: Lista todas as categorias.
  - Response: Lista de strings.

- **GET /api/v1/health**: Status da API.
  - Response: {"status": "ok"}
'''

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
#from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from prometheus_fastapi_instrumentator import Instrumentator
import fiap_tech_cha_fase1.app.v1.routers.livros as livros
import fiap_tech_cha_fase1.app.v1.routers.stats as stats

app = FastAPI(title="FIAP Tech Challenge - Fase 1", version="1.0.0")

# Adiciona os routers de livros
app.include_router(livros.router)
app.include_router(stats.router)

# router health
@app.get("/api/v1/health", include_in_schema=True, tags=["infra"])
async def health():
    return {"status": "ok"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
)

# Instrumentação Prometheus
Instrumentator().instrument(app).expose(app)