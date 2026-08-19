# Project Conventions

## Código

- Código, nomes de classes, funções e variáveis em inglês.
- Documentação de produto pode ser escrita em português.
- Funções pequenas e responsabilidades claras.
- Regras de decisão devem ser isoladas de I/O sempre que possível.
- Evitar lógica de negócio diretamente em endpoints.

## Estrutura

O monorepo organiza componentes independentes em `services/`. O serviço de analytics é responsável por coleta, normalização, domínio, métricas, regras e futuros modelos estatísticos. A futura interface desktop deve consumir contratos estáveis do serviço, sem duplicar lógica analítica.

## Qualidade

Antes de cada commit relevante no analytics:

```bash
uv run ruff check .
uv run pytest
```

A cobertura mínima configurada é 90%.

## Git

Usar commits pequenos e objetivos, preferencialmente no formato:

```text
feat: add match state model
fix: normalize item identifiers
test: cover recommendation rule
docs: document data source decision
refactor: isolate scoring logic
```

Não versionar arquivos gerados localmente, cobertura, ambientes virtuais, caches ou credenciais.

## Dados e fair play

- Não coletar informações que o jogador não deveria conhecer.
- Não automatizar ações no cliente do jogo.
- Toda nova fonte de dados deve ser documentada antes da integração.
- Recomendações devem ser reproduzíveis a partir do estado conhecido da partida.
- Modelos de ML não substituem validação de regras e métricas básicas.

## Arquitetura

Mudanças estruturais importantes devem ganhar um registro em `docs/decisions/` explicando contexto, decisão e consequências.
