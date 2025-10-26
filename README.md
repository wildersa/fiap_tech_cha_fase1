# fiap-tech-cha-fase1

## Descrição do Projeto

Entrega do **Tech Challenge - Fase 1 (Machine Learning Engineering)**: construir um pipeline (ingestão → processamento → API) para disponibilizar dados de livros extraídos via web scraping e prontos para consumo por times de ML e sistemas de recomendação.

Resumo rápido:

- Fonte de dados: <https://books.toscrape.com/>
- Formato de saída principal: CSV (local)
- API: RESTful (FastAPI ou Flask) com documentação OpenAPI/Swagger

## Entregáveis obrigatórios (síntese)

1. Repositório GitHub organizado (módulos: `scripts/`, `api/`, `data/`, etc.).
2. Sistema de Web Scraping:
   - Script capaz de extrair todos os livros do site alvo.
   - Campos obrigatórios: título, preço, rating, disponibilidade, categoria, imagem (URL ou arquivo local).
   - Dados armazenados localmente em CSV.
3. API RESTful funcional (FastAPI ou Flask) com os endpoints obrigatórios descritos abaixo e documentação OpenAPI/Swagger.
4. Deploy público (Heroku/Render/Vercel/Fly.io ou similar) com link funcional (entregável obrigatório).
5. Plano arquitetural (diagrama/documento) descrevendo pipeline e escolhas arquiteturais para escalabilidade.
6. Vídeo de apresentação (3–12 minutos) demonstrando arquitetura e chamadas reais à API em produção.

> Para os detalhes completos e o texto original dos requisitos veja `docs/Pos_tech`.

## Endpoints obrigatórios

- GET /api/v1/books — lista todos os livros.
- GET /api/v1/books/{id} — detalhes de um livro pelo ID.
- GET /api/v1/books/search?title={title}&category={category} — busca por título e/ou categoria.
- GET /api/v1/categories — lista todas as categorias.
- GET /api/v1/health — status da API.

Resposta esperada (forma geral): JSON com campos representativos (id, title, price, rating, availability, category, image).
