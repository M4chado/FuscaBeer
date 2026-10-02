# AGENTS.md — micro-SaaS Fusca Beer

Registro de vendas e fechamento de caixa do Fusca Beer. Disciplina ESW442 (UniRV).

## Stack
Python 3.13 · Django 6.1 · PostgreSQL 17 · templates + HTMX · pytest + pytest-django · behave + behave-django · ruff

## Como rodar (do zero)
```bash
cp .env.example .env              # depois troque as senhas
docker compose up -d db           # PostgreSQL 17 em localhost:5432
python3.13 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver        # http://localhost:8000
```

## Como testar (passa antes de todo commit)
```bash
ruff check . && ruff format --check .   # lint e formatação
pytest                                  # testes de unidade em tests/
python manage.py behave                 # critérios de aceite em features/
```

## Estrutura
- `config/` configuração do Django · `tests/` pytest · `features/` cenários Gherkin (`# language: pt`)
- `docs/specs/` specs das features (fonte da verdade) · `docs/harness/` relatórios e evidências do harness
- Cada app de feature fica na raiz (ex.: `vendas/`), criado quando a spec dela for implementada.

## Regras
- Toda feature nova começa por uma spec em `docs/specs/NNN-<feature>.md`.
- Não altere `docs/specs/` sem aviso: a spec é a fonte da verdade. Proponha a mudança.
- Cada critério de aceite (CA-xx) vira um cenário em `features/NNN-<feature>.feature` com o mesmo ID no nome.
- Valores em R$ são inteiros em centavos. Datas usam `America/Sao_Paulo`.
- Segredos só no `.env`, que não vai para o Git e é bloqueado nas permissões. Para saber as variáveis, leia `.env.example`.
- Commit cita spec e critério: `feat(001): calcula troco em dinheiro (CA-02)`.
- Servidores MCP: nenhum instalado.

## Como você deve trabalhar
- Declare suas suposições. Se o pedido admite duas leituras, pergunte antes de escolher uma.
- O mínimo que resolve. Sem abstração de uso único, sem opção que ninguém pediu, sem tratar erro que não acontece.
- Toque só no necessário. Mantenha o estilo do arquivo e não refatore código que funciona e não faz parte do pedido.
- Diga como vai provar que funcionou, e rode a prova antes de dizer que terminou.
