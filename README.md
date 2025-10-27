# fiap-tech-cha-fase1

## Descrição do Projeto

Entrega do **Tech Challenge - Fase 1 (Machine Learning Engineering)**: construir um pipeline (ingestão → processamento → API) para disponibilizar dados de livros extraídos via web scraping e prontos para consumo por times de ML e sistemas de recomendação.

Resumo rápido:

- Fonte de dados: <https://books.toscrape.com/>
- Formato de saída principal: CSV (local)
- API: RESTful (FastAPI ou Flask) com documentação OpenAPI/Swagger

## Instruções de instalação e configuração

### Requisitos

- Python 3.11 ou superior
- Poetry

### .env

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

```env
APP_NAME=fiap_tech_cha_fase1
HOST=127.0.0.1
PORT=8000
RELOAD=False
LOG_LEVEL=info
APP_IMPORT_PATH=fiap_tech_cha_fase1.app.main:app
```

### Executando a aplicação

Para utilizar a ferramenta é possível usar o Poetry, com os seguintes comandos:

```bash
poetry install
poetry run python -m fiap_tech_cha_fase1
```

ou usando instalando as dependencias diretamente com o pip:

```bash
pip install -r requirements.txt
python -m fiap_tech_cha_fase1
```

A aplicação estará disponível em `http://127.0.0.1:8000`.

## Rotas da API

- Documentação automática: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

### Rotas obrigatórias

- GET `/api/v1/books` — lista todos os livros.
- GET `/api/v1/books/{id}` — detalhes de um livro pelo ID.
- GET `/api/v1/books/search?title={title}&category={category}` — busca por título e/ou categoria.
- GET `/api/v1/categories` — lista todas as categorias.
- GET `/api/v1/health` — status da API.

### Exemplos de chamadas com requests/responses

#### GET `/api/v1/books`

- Listar todos os livros:

Request:

  ```bash
  curl http://127.0.0.1:8000/api/v1/books
  ```

Response:

  ```json
  [
    {
      "id": "23356462d1320d61",
      "title": "In Her Wake",
      "price": "£12.84",
      "rating": "One",
      "availability": "In stock",
      "category": "Thriller",
      "local_image": "data\\imagens\\23356462d1320d61.jpg"
    },
    {
      "id": "5dada2b7be26bd03",
      "title": "The Elephant Tree",
      "price": "£23.82",
      "rating": "Five",
      "availability": "In stock",
      "category": "Thriller",
      "local_image": "data\\imagens\\5dada2b7be26bd03.jpg"
    }
  ]
  ```

#### GET `/api/v1/books/{id}`

- Retornar detalhes de um livro específico pelo ID.

Request:

```bash
curl http://127.0.0.1:8000/api/v1/books/23356462d1320d61
```

Response:

```json
{
  "id": "23356462d1320d61",
  "title": "In Her Wake",
  "price": "£12.84",
  "rating": "One",
  "availability": "In stock",
  "local_image": "data\\imagens\\23356462d1320d61.jpg"
}
```

#### GET `/api/v1/books/search?title={title}&category={category}`

- Buscar livros por título e/ou categoria.

Request:

```bash
curl "http://127.0.0.1:8000/api/v1/books/search?title=In Her Wake&category=Thriller"
```

Response:

```json
[
  {
    "id": "23356462d1320d61",
    "title": "In Her Wake",
    "price": "£12.84",
    "rating": "One",
    "availability": "In stock",
    "local_image": "data\\imagens\\23356462d1320d61.jpg"
  }
]
```

#### GET `/api/v1/categories`

- Listar todas as categorias de livros.

Request:

```bash
curl http://127.0.0.1:8000/api/v1/categories
```

Response:

```json
[
  {
    "id": "1",
    "name": "Category 1"
  },
  {
    "id": "2",
    "name": "Category 2"
  }
]
```

#### GET `/api/v1/health`

- Verificar o status da API.

Request:

```bash
curl http://127.0.0.1:8000/api/v1/health
```

Response:

```json
{
  "status": "ok"
}
```

## Instruções para execução

### Scraper

Para executar o scraper e gerar o arquivo CSV com os dados dos livros, siga os passos abaixo:

1. Navegue até o diretório do projeto:

   ```bash
   cd /dev/fiap_tech_cha_fase1
   ```

2. Execute o script do scraper:

   ```bash
   python -m fiap_tech_cha_fase1.scripts.scraper
   ```

Desições e funcionamento:

Foi usado o id do próprio site `upc` como id único de cada livro.
O scraper cria um arquivo `livros.csv` dentro da pasta `data/`.
As imagens são salvas dentro de `data\imagens` onde o nome da imagem é o ID do livro.
Há uma função de não baixar imagem repetida pra reaproveitar caso já exista.

## Autor

Wilder Schmidt Andreatta
