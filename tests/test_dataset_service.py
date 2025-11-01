from pathlib import Path
from fiap_tech_cha_fase1.app.services.dataset_service import carregar_livros_raw, carregar_livros_normalizados

CSV_TXT = """titulo,preco,rating,disponibilidade,categoria
Book A,£10.50,Three,In stock (5 available),Fiction
Book B,£20,Five,In stock (1 available),Drama
"""

def test_carregar_livros_raw(tmp_path: Path):
    p = tmp_path / "livros.csv"
    p.write_text(CSV_TXT, encoding="utf-8")

    rows = carregar_livros_raw(p)
    assert isinstance(rows, list)
    assert len(rows) == 2
    assert rows[0]["preco"] == "£10.50"

def test_carregar_livros_normalizados(tmp_path: Path):
    p = tmp_path / "livros.csv"
    p.write_text(CSV_TXT, encoding="utf-8")

    rows = carregar_livros_normalizados(p)
    a, b = rows[0], rows[1]

    assert a["preco"] == 10.50
    assert a["rating"] == 3
    assert b["preco"] == 20.0
    assert b["rating"] == 5
