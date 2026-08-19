# RiftPilot

RiftPilot é um projeto experimental de **assistente analítico para League of Legends**, pensado como aplicativo desktop com foco em análise de contexto, recomendações explicáveis e apoio à tomada de decisão usando apenas informações permitidas e disponíveis ao próprio jogador.

> Status: em desenvolvimento. O repositório contém a fundação técnica do serviço de analytics; as funcionalidades de recomendação em tempo real ainda não estão concluídas.

## Objetivo

O projeto explora como dados, regras de decisão e modelos estatísticos podem ser usados para transformar o estado de uma partida em recomendações úteis, como:

- interpretação de matchup;
- sugestões de build condicionais ao contexto;
- leitura de objetivos e janelas de rotação;
- análise pós-partida;
- explicação do motivo de cada recomendação.

RiftPilot não pretende obter informações ocultas da partida ou automatizar ações dentro do jogo.

## Princípios do produto

1. **Fair play primeiro** — usar somente dados disponíveis ao jogador e fontes permitidas.
2. **Recomendações explicáveis** — cada sugestão deve ter contexto e justificativa.
3. **Analytics antes de IA** — começar por coleta, normalização, regras e métricas; modelos mais complexos entram quando houver dados e validação suficientes.
4. **Local-first quando possível** — o serviço de análise roda localmente e pode ser consumido pelo futuro aplicativo desktop.
5. **Arquitetura modular** — separar ingestão, domínio, regras, modelos e interface.

## Estado atual

A primeira peça implementada é o serviço `services/analytics`:

- Python 3.13;
- FastAPI;
- Pydantic;
- `uv` para dependências;
- Ruff para lint;
- Pytest + cobertura mínima de 90%;
- endpoint de health check;
- estrutura pronta para receber coleta, normalização e regras de decisão.

## Arquitetura planejada

```text
League Client / fontes permitidas
            │
            ▼
     Data Collection
            │
            ▼
      Normalization
            │
            ▼
   Match State / Domain
       │           │
       ▼           ▼
 Decision Rules   Models
       │           │
       └─────┬─────┘
             ▼
 Recommendation Engine
             │
             ▼
       Desktop Client
```

A prioridade é construir primeiro uma representação confiável do estado da partida. A camada de recomendação só deve consumir dados normalizados e testáveis.

## Estrutura

```text
riftpilot/
├── docs/
│   ├── decisions/          # decisões de arquitetura
│   ├── development-setup.md
│   └── roadmap.md
├── services/
│   └── analytics/          # serviço Python/FastAPI
├── scripts/
├── PROJECT_CONVENTIONS.md
└── README.md
```

## Executando o serviço de analytics

```bash
cd services/analytics
uv sync --group dev
uv run ruff check .
uv run pytest
uv run uvicorn riftpilot_analytics.main:app --reload
```

API local:

```text
http://127.0.0.1:8000
```

Documentação OpenAPI:

```text
http://127.0.0.1:8000/docs
```

## Roadmap resumido

- [x] Estrutura inicial do monorepo
- [x] Serviço Python de analytics
- [x] Health check, testes, lint e cobertura
- [ ] Definir modelo de domínio da partida
- [ ] Camada de ingestão de dados permitidos
- [ ] Normalização de campeões, itens e eventos
- [ ] Motor inicial de regras explicáveis
- [ ] Matchup scoring
- [ ] Recomendações condicionais de build
- [ ] Análise de objetivos e rotações
- [ ] Persistência local de partidas
- [ ] Cliente desktop
- [ ] Modelos estatísticos/ML após validação da base

Veja [`docs/roadmap.md`](docs/roadmap.md) para o plano detalhado.

## O que este projeto demonstra

RiftPilot é principalmente um projeto de **Dados + Backend + Produto**. Ele foi criado para praticar modelagem de domínio, APIs locais, pipelines de dados, testes, estatística aplicada e, futuramente, machine learning em um problema com decisões em tempo real.

## Aviso

League of Legends e Riot Games são marcas de seus respectivos proprietários. RiftPilot é um projeto independente de estudo e portfólio e não possui afiliação oficial com a Riot Games.
