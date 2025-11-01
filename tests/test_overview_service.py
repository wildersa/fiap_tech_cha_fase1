from fiap_tech_cha_fase1.app.services.stats_service import computar_estatisticas_overview

def test_computar_estatisticas_ok():
    livros = [
        {"preco": 10.5, "rating": 3},
        {"preco": 20.0, "rating": 5},
        {"preco": 19.5, "rating": 5},
    ]
    r = computar_estatisticas_overview(livros)
    assert r["total_livros"] == 3
    assert r["preco_medio"] == 16.67  # (10.5+20+19.5)/3 = 16.6667
    assert r["distribuicao_ratings"] == {3:1, 5:2}

def test_computar_estatisticas_vazio():
    r = computar_estatisticas_overview([])
    assert r == {"total_livros": 0, "preco_medio": 0.0, "distribuicao_ratings": {}}
