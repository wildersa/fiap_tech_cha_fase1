"""
Testes para o scraper de livros.
Usa pytest e unittest.mock para simular requests e BeautifulSoup.
"""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from bs4 import BeautifulSoup
import csv
import tempfile

# Importar apenas as funções, não o módulo inteiro para evitar execução
from fiap_tech_cha_fase1.scripts.scraper import (
    baixar_imagem,
    extrair_dados_livro,
    pegar_upc_da_pagina
)

# Importar do service
from fiap_tech_cha_fase1.app.services.livros_service import (
    listar_livros,
    obter_livro_por_id,
    buscar_livros,
    listar_categorias
)

# Fixture para mockar session
@pytest.fixture
def mock_session():
    session = MagicMock()
    return session

# Teste para baixar_imagem
def test_baixar_imagem_sucesso(mock_session):
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"fake image data"
    mock_session.get.return_value = mock_response

    # Mock Path
    with tempfile.TemporaryDirectory() as temp_dir:
        mock_imagens_dir = Path(temp_dir) / "imagens"
        mock_imagens_dir.mkdir()

        with patch('fiap_tech_cha_fase1.scripts.scraper.IMAGENS_DIR', mock_imagens_dir):
            with patch('fiap_tech_cha_fase1.scripts.scraper.PACOTE_ROOT', Path(temp_dir)):
                result = baixar_imagem("http://example.com/image.jpg", "test_id", session=mock_session)

                expected = Path("imagens/test_id.jpg")
                assert Path(result) == expected
                mock_session.get.assert_called_once_with("http://example.com/image.jpg", timeout=(3, 10))
                assert (mock_imagens_dir / "test_id.jpg").exists()

def test_baixar_imagem_falha(mock_session):
    mock_session.get.side_effect = Exception("Network error")

    result = baixar_imagem("http://example.com/image.jpg", "test_id", session=mock_session)
    assert result is None

# Teste para extrair_dados_livro
def test_extrair_dados_livro():
    html = '''
    <article class="product_pod">
        <h3><a href="../catalogue/test-book/index.html" title="Test Book">Test Book</a></h3>
        <p class="price_color">$10.00</p>
        <p class="star-rating One">One</p>
        <p class="instock availability">In stock</p>
    </article>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('article')

    with patch('fiap_tech_cha_fase1.scripts.scraper.pegar_upc_da_pagina', return_value="12345"):
        with patch('fiap_tech_cha_fase1.scripts.scraper.baixar_imagem', return_value="data/imagens/12345.jpg"):
            with patch('fiap_tech_cha_fase1.scripts.scraper.session') as mock_session:
                mock_resp = MagicMock()
                mock_resp.text = '<div class="thumbnail"><img src="image.jpg"></div>'
                mock_session.get.return_value = mock_resp
                result = extrair_dados_livro(article, "Test Category")

                assert result is not None
                assert result['titulo'] == "Test Book"
                assert result['preco'] == "$10.00"
                assert result['rating'] == "One"
                assert result['categoria'] == "Test Category"

# Teste para pegar_upc_da_pagina
def test_pegar_upc_da_pagina(mock_session):
    html = '''
    <table>
        <tr><th>UPC</th><td>123456789</td></tr>
    </table>
    '''
    mock_response = MagicMock()
    mock_response.text = html
    mock_session.get.return_value = mock_response

    result = pegar_upc_da_pagina("http://example.com/book", session=mock_session)
    assert result == "123456789"

# Testes para service (usando CSV mockado)
@pytest.fixture
def mock_csv(tmp_path):
    csv_path = tmp_path / "livros.csv"
    data = [
        {'id': '1', 'titulo': 'Book 1', 'categoria': 'Fiction'},
        {'id': '2', 'titulo': 'Book 2', 'categoria': 'Non-Fiction'},
    ]
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'titulo', 'categoria'])
        writer.writeheader()
        writer.writerows(data)
    return data  # Retorna os dados mock

def test_listar_livros(monkeypatch, mock_csv):
    monkeypatch.setattr('fiap_tech_cha_fase1.app.services.dataset_service.carregar_livros_raw', lambda: mock_csv)
    livros = listar_livros()
    assert len(livros) == 2
    assert livros[0]['titulo'] == 'Book 1'

def test_obter_livro_por_id(monkeypatch, mock_csv):
    monkeypatch.setattr('fiap_tech_cha_fase1.app.services.dataset_service.carregar_livros_raw', lambda: mock_csv)
    livro = obter_livro_por_id('1')
    assert livro['titulo'] == 'Book 1'
    assert obter_livro_por_id('999') is None

def test_buscar_livros(monkeypatch, mock_csv):
    monkeypatch.setattr('fiap_tech_cha_fase1.app.services.dataset_service.carregar_livros_raw', lambda: mock_csv)
    results = buscar_livros(titulo='Book')
    assert len(results) == 2
    results = buscar_livros(categoria='Fiction')
    assert len(results) == 1

def test_listar_categorias(monkeypatch, mock_csv):
    monkeypatch.setattr('fiap_tech_cha_fase1.app.services.dataset_service.carregar_livros_raw', lambda: mock_csv)
    categorias = listar_categorias()
    assert 'Fiction' in categorias
    assert 'Non-Fiction' in categorias