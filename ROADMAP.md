# ROADMAP

## Visão Geral

Este roadmap descreve a evolução planejada do projeto **API Pública de Livros**, desenvolvido como parte do Tech Challenge – Machine Learning Engineering (Fase 1).  
O objetivo é entregar uma API escalável, baseada em dados coletados de forma automatizada, servindo como base para modelos de recomendação e consumo por cientistas de dados.

---

## Fase 1 – MVP (04 a 06/out)

**Objetivo:** Entregar um pipeline funcional de ponta a ponta.

### Entregas - Fase 1

- [ ] Criar repositório GitHub com estrutura base (`scripts/`, `api/`, `data/`, `docs/`).
- [ ] Implementar scraper de `books.toscrape.com` com extração completa.
- [ ] Armazenar dados em `data/books.csv`.
- [ ] Criar API com FastAPI e endpoints:
  - `/api/v1/health`
  - `/api/v1/books`
  - `/api/v1/books/{id}`
  - `/api/v1/books/search`
  - `/api/v1/categories`
- [ ] Deploy público (Render/Vercel/Fly.io).
- [ ] README com exemplos e documentação Swagger.
- [ ] Vídeo de apresentação (5–8 min).
- [ ] Arquitetura/diagrama do pipeline.

---

## Fase 2 – Insights (07 a 10/out)

**Objetivo:** Enriquecer a API com endpoints analíticos e métricas.

### Entregas - Fase 2

- [ ] `/api/v1/stats/overview`
- [ ] `/api/v1/stats/categories`
- [ ] `/api/v1/books/top-rated`
- [ ] `/api/v1/books/price-range`
- [ ] Logging estruturado e métricas básicas (tempo de resposta, contagem de chamadas).

---

## Fase 3 – ML Ready (11 a 13/out)

**Objetivo:** Preparar dados e endpoints para consumo por modelos de Machine Learning.

### Entregas - Fase 3

- [ ] `/api/v1/ml/features` – features estruturadas.
- [ ] `/api/v1/ml/training-data` – dataset de treino.
- [ ] `/api/v1/ml/predictions` – endpoint para previsões.
- [ ] Documentar plano de integração com modelos futuros.

---

## Fase 4 – Extra (Opcional)

**Objetivo:** Agregar valor adicional ao projeto e obter pontos bônus.

### Entregas - Fase Extra

- [ ] Implementar autenticação JWT para rotas administrativas.
- [ ] Criar dashboard simples de monitoramento (Streamlit).
- [ ] Realizar curso **“Use Machine Learning APIs on Google Cloud”** e anexar certificado.
- [ ] Revisar documentação final e diagrama atualizado.

---

## Status Geral

| Fase | Período | Status | Progresso |
|------|----------|---------|-----------|
| MVP | 04–06/out | 🔄 Em execução | 60% |
| Insights | 07–10/out | ⏳ Planejado | 0% |
| ML Ready | 11–13/out | ⏳ Planejado | 0% |
| Extra | até 15/out | ⏳ Opcional | - |

---

## Próximos Passos

- Finalizar deploy e gravação do vídeo.  
- Iniciar endpoints de estatísticas e preparar estrutura ML.  
- Consolidar documentação para entrega final.
