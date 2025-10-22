# fiap-tech-cha-fase1

## Observação importante — fonte de verdade

O documento canônico com os requisitos e critérios do Tech Challenge está em `docs/Pos_tech - Tech Challenge - Fase 1 - Machine Leanring Engineering.md` (abreviado como `docs/Pos_tech`). Este `README.md` foi revisado para focar nos requisitos obrigatórios; instruções de instalação, execução e deploy permanecem em rascunho.

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

### Endpoints opcionais (recomendados para bônus)

- GET /api/v1/stats/overview — estatísticas gerais (total de livros, preço médio, distribuição de ratings).
- GET /api/v1/stats/categories — estatísticas por categoria.
- GET /api/v1/books/top-rated — livros com melhor rating.
- GET /api/v1/books/price-range?min={min}&max={max} — filtrar por faixa de preço.

## Dados a serem extraídos (campos mínimos)

- id (gerado)
- title
- price (valor numérico)
- rating (p.ex. 1-5)
- availability (ex.: In stock/Out of stock, quantidade quando possível)
- category
- image (URL ou caminho local)

## Instalação & Execução (RASUNHO)

OBS: Esta seção está marcada como rascunho — o foco do repositório e da entrega é cumprir os requisitos acima. Instruções detalhadas serão adicionadas em seguida; enquanto isso, um fluxo mínimo:

1) Clonar repositório e instalar dependências (ex.: Poetry).
2) Executar script de scraping para gerar `src/fiap_tech_cha_fase1/data/livros.csv` (ou `data/livros.csv`).
3) Executar a API localmente (ex.: Uvicorn para FastAPI ou python para Flask).

As instruções completas e comandos exatos estão em rascunho — ver `docs/Pos_tech` para referência imediatamente disponível.

## Documentação e validação

- A API deve expor documentação OpenAPI/Swagger (ex.: `/docs` no FastAPI).
- Testes mínimos esperados: endpoints obrigatórios retornando os formatos corretos e health check com status OK.

## Plano arquitetural & Diagrama

Ver `docs/Pos_tech` para o diagrama completo e justificativas arquiteturais.

## Vídeo de Apresentação

Inserir link do vídeo (3–12 minutos) que demonstre chamadas reais à API em produção e explique a arquitetura.

## Contribuição

Desenvolvido por Wilder Andreatta.

Para dúvidas, abra uma issue no GitHub.

## Licença

Projeto para fins educacionais.
