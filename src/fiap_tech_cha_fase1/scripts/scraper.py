"""
Web Scraping Robusto:

• Extrair todos os livros disponíveis no site. 
• Capturar: título, preço, rating, disponibilidade, categoria, imagem.
• Salvar em CSV na pasta data.

URL: https://books.toscrape.com/
"""
import logging
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import csv
from pathlib import Path
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionado session pois sem fica muito lento e falha com muitas requisições
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})
retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500,502,503,504], raise_on_status=False)
adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
session.mount("http://", adapter)
session.mount("https://", adapter)

debug_interno = False

def debug_print(msg, *args, **kwargs):
    if debug_interno:
        print(msg.format(*args, **kwargs))

# Inicia a medição do tempo
tempo_inicio = time.time()

BASE_URL = "https://books.toscrape.com/"
response = session.get(BASE_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Pasta do pacote
PACOTE_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PACOTE_ROOT / 'data'
IMAGENS_DIR = DATA_DIR / 'imagens'
CSV_PATH = DATA_DIR / 'livros.csv'

IMAGENS_DIR.mkdir(parents=True, exist_ok=True)

# Função para baixar e salvar imagem
def baixar_imagem(imagem_url, livro_id, session=None, timeout=(3,10)):
    nome_arquivo = f"{livro_id}.jpg"
    caminho = IMAGENS_DIR / nome_arquivo

    # já existe? sai antes de qualquer HTTP. Estava muito lento e falhando
    if caminho.exists():
        return str(caminho.relative_to(PACOTE_ROOT))  # "data/imagens/xxx.jpg"

    s = session or requests
    for attempt in range(2):
        try:
            r = s.get(imagem_url, timeout=timeout)
            if r.status_code == 200:
                caminho.write_bytes(r.content)
                baixar_imagem.contador_salvas = getattr(baixar_imagem, 'contador_salvas', 0) + 1
                return str(caminho.relative_to(PACOTE_ROOT))
            time.sleep(1)
        except Exception as e:
            debug_print(f"Tentativa {attempt+1} falhou p/ {livro_id}: {e}")
            time.sleep(1)
    debug_print(f"Falhou após 2 tentativas p/ {livro_id}.")
    return None

# Função para extrair dados de um livro
def extrair_dados_livro(book_soup, categoria):
    try:
        titulo = book_soup.h3.a['title']
        preco = book_soup.find('p', class_='price_color').text.encode('latin1').decode('utf-8').strip() # Arrumar caractere que vem no preço.
        rating_class = book_soup.find('p', class_='star-rating')['class']
        rating = rating_class[1] if len(rating_class) > 1 else 'Sem rating'
        disponibilidade = book_soup.find('p', class_='instock availability').text.strip()
        # Extrair ID único do livro e montar URL da página de detalhe
        livro_href = book_soup.h3.a['href']
        # limpar '../' do início do href e garantir /catalogue/ no caminho
        href_clean = livro_href
        while href_clean.startswith('../'):
            href_clean = href_clean[3:]
        livro_id = href_clean.split('/')[-2]  # Pega o penúltimo elemento (antes de /index.html)
        # URL da página de detalhe do livro
        detalhe_url = urljoin(BASE_URL + 'catalogue/', href_clean)
        

        # Acessar página de detalhe para pegar a imagem completa (não a thumb)
        try:
            detalhe_resp = session.get(detalhe_url)
            detalhe_soup = BeautifulSoup(detalhe_resp.text, 'html.parser')
            # A imagem grande fica dentro da div.thumbnail (na página de detalhe)
            img_tag = detalhe_soup.find('div', class_='thumbnail')
            if img_tag:
                img_elem = img_tag.find('img')
                if img_elem and img_elem.get('src'):
                    img_rel = img_elem['src']
                    imagem_url = urljoin(detalhe_url, img_rel)
                else:
                    imagem_url = None
            else:
                imagem_url = None
        except Exception:
            imagem_url = None

        try:
            upc = pegar_upc_da_pagina(detalhe_url, session=session)
        except Exception:
            upc = None
        id_upc = upc

        # Baixar imagem usando o ID como nome (se tivermos uma URL válida)
        imagem_local = None
        if imagem_url:
            imagem_local = baixar_imagem(imagem_url, upc, session=session)
        
        return {
            'id': id_upc,
            'titulo': titulo,
            'preco': preco,
            'rating': rating,
            'disponibilidade': disponibilidade,
            'categoria': categoria,
            'imagem_url': imagem_url,
            'imagem_local': imagem_local
        }
    except (AttributeError, KeyError, TypeError, IndexError):
        return None

# Vou usar o UPC como ID único.
def pegar_upc_da_pagina(detalhe_url, session=None):
    response = session.get(detalhe_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    UPC = soup.find('th', string='UPC')
    return UPC.find_next_sibling('td').text.strip() if UPC else None

# Lista para armazenar todos os livros
livros = []

# Contadores de imagens (tentadas e salvas)
baixar_imagem.contador_tentadas = 0
baixar_imagem.contador_salvas = 0

# Pegar todas as categorias
categorias = soup.find('ul', class_='nav-list').find('ul').find_all('li')
debug_print(f"Encontradas {len(categorias)} categorias.")

total_categorias = len(categorias)
# processed_categories = 0

# Iterar sobre categorias e pegar dados dos livros
for idx, cat in enumerate(categorias, start=1):
    cat_nome = cat.a.text.strip()
    cat_url_relativa = cat.a['href']
    cat_url = urljoin(BASE_URL, cat_url_relativa)
    
    # Acessar página da categoria
    cat_resposta = session.get(cat_url)
    cat_soup = BeautifulSoup(cat_resposta.text, 'html.parser')

    # Descobrir número de páginas
    pagina_corrente = cat_soup.find('li', class_='current')
    if pagina_corrente:
        pagina_texto = pagina_corrente.text.strip()
        pagina_texto_split = pagina_texto.split()
        try:
            primeira_pagina = int(pagina_texto_split[1])
            ultima_pagina = int(pagina_texto_split[3])
        except (IndexError, ValueError):
            primeira_pagina = ultima_pagina = 1
    else:
        primeira_pagina = ultima_pagina = 1
    
    # Pegar livros de cada página
    for pagina in range(primeira_pagina, ultima_pagina + 1):
        if pagina == 1:
            url_pagina = cat_url
        else:
            url_pagina = cat_url.replace('index.html', f'page-{pagina}.html')
        response = session.get(url_pagina)
        soup = BeautifulSoup(response.text, 'html.parser')

        livros_na_pagina = soup.find_all('article', class_='product_pod')
        for book_soup in livros_na_pagina:
            dados_livro = extrair_dados_livro(book_soup, cat_nome)
            # incrementar tentativas quando houver URL de imagem
            if dados_livro and dados_livro.get('imagem_url'):
                baixar_imagem.contador_tentadas += 1
            if dados_livro:
                livros.append(dados_livro)
    
    # Barra de progresso global por categoria
    progresso = (idx / total_categorias) * 100
    barra = '#' * int(progresso / 10) + ' ' * (10 - int(progresso / 10))
    debug_print(f'\r[{barra}] {progresso:.1f}% - Categoria {cat_nome} processada, total livros: {len(livros)}', end='', flush=True)
    

# Salvar em CSV
with CSV_PATH.open(mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['id', 'titulo', 'preco', 'rating', 'disponibilidade', 'categoria', 'imagem_local'],
                            extrasaction='ignore')
    writer.writeheader()
    writer.writerows(livros)
debug_print(f"\nDados salvos em {CSV_PATH}")

# Calcula e imprime o tempo total
tempo_fim = time.time()
tempo_total = tempo_fim - tempo_inicio

# Resumo de imagens
debug_print(f"Imagens tentadas: {baixar_imagem.contador_tentadas} | Imagens salvas: {baixar_imagem.contador_salvas}")
debug_print(f"\nTempo total {tempo_total:.2f} segundos.")