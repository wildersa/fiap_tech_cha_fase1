"""
Testes para os endpoints de livros usando httpx e FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient
import csv
from fiap_tech_cha_fase1.app.main import app  # importa a app FastAPI

# Fixture para mockar o CSV
@pytest.fixture
def mock_csv(tmp_path):
    csv_path = tmp_path / "livros.csv"
    data = [
        {'id': '1', 'titulo': 'Book 1', 'preco': '£10.00', 'rating': 'One', 'disponibilidade': 'In stock', 'categoria': 'Fiction', 'imagem_local': 'data/imagens/1.jpg'},
        {'id': '2', 'titulo': 'Book 2', 'preco': '£20.00', 'rating': 'Two', 'disponibilidade': 'In stock', 'categoria': 'Non-Fiction', 'imagem_local': 'data/imagens/2.jpg'},
    ]
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'titulo', 'preco', 'rating', 'disponibilidade', 'categoria', 'imagem_local'])
        writer.writeheader()
        writer.writerows(data)
    return csv_path

# Fixture para TestClient
@pytest.fixture
def client(mock_csv):
    # Mock o path do CSV
    from fiap_tech_cha_fase1.app.services import livros_service
    livros_service.DEFAULT_CSV = mock_csv
    return TestClient(app)

# Teste para GET /api/v1/books
def test_lista_livros(client):
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['titulo'] == 'Book 1'

# Teste para GET /api/v1/books/{id}
def test_detalhes_livro(client):
    response = client.get("/api/v1/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data['titulo'] == 'Book 1'

    # Livro não encontrado
    response = client.get("/api/v1/books/999")
    assert response.status_code == 404

# Teste para GET /api/v1/books/search
def test_busca_livros(client):
    # Busca por título
    response = client.get("/api/v1/books/search?title=Book")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Busca por categoria
    response = client.get("/api/v1/books/search?category=Fiction")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['categoria'] == 'Fiction'

    # Busca sem resultados
    response = client.get("/api/v1/books/search?title=Nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

# Teste para GET /api/v1/categories
def test_lista_categorias(client):
    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert 'Fiction' in data
    assert 'Non-Fiction' in data

# Teste para GET /api/v1/health
def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'ok'