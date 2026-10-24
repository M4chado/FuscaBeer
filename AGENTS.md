# AGENTS.md — micro-SaaS Fusca Beer

Registro de vendas e fechamento de caixa do Fusca Beer. Disciplina ESW442 (UniRV).

## Stack
Python 3.13 · Django 6.1 · PostgreSQL 17 · templates + HTMX · pytest + pytest-django · behave + behave-django · ruff

## Como rodar (do zero)
```bash
cp .env.example .env              # depois troque as senhas
                                  # banco: veja "Banco de dados" abaixo (Docker ou PostgreSQL 17 local)
python3.13 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # o login único do operador (D-04); pede usuário e senha
python manage.py runserver        # http://localhost:8000 → entre com esse login
```
### Banco de dados (PostgreSQL 17 em localhost:5432; use um dos dois)
- **Docker:** `docker compose up -d db`
- **Local (sem Docker):** instale o PostgreSQL 17 e crie o usuário e o banco com os valores do `.env`:
  ```sql
  CREATE USER fuscabeer WITH PASSWORD 'a-senha-do-seu-.env' CREATEDB;  -- CREATEDB: o pytest cria um banco de teste
  CREATE DATABASE fuscabeer OWNER fuscabeer;
  ```

Depois de entrar: cadastre os produtos em **Produtos** e registre vendas em **Nova venda**.

## Como testar
```bash
ruff check . && ruff format --check .   # lint e formatação
pytest                                  # testes de unidade em tests/
python manage.py behave                 # critérios de aceite em features/
python manage.py makemigrations --check --dry-run   # modelos e migrações em sincronia
```
Esta é a única definição de pronto para os commits de verde (`feat`) e de refatoração (`refactor`): os quatro comandos passando. A skill e o CLAUDE.md apontam para cá.

Exceção: no commit do vermelho (`test(NNN): ... (CA-xx)`), tudo passa menos o cenário ou teste novo daquele CA. Ele precisa falhar pelo motivo esperado (ex.: 404 da rota que não existe, `AttributeError`), e os testes antigos continuam verdes.

## Estrutura
- `config/` configuração do Django · `tests/` pytest · `features/` cenários Gherkin (`# language: pt`)
- `templates/` base das telas e login · `static/js/` HTMX vendorizado (não baixa nada da internet)
- `vendas/regras.py` cálculos puros (total, troco, dia de operação, totais) · `vendas/views.py` rotas da seção 7 da spec
- `docs/specs/` specs das features (fonte da verdade) · `docs/harness/` relatórios e evidências do harness
- Cada app de feature fica na raiz (ex.: `vendas/`), criado quando a spec dela for implementada.

## Regras
- Toda feature nova começa por uma spec em `docs/specs/NNN-<feature>.md`.
- Não altere `docs/specs/` sem aviso: a spec é a fonte da verdade. Proponha a mudança.
- Cada critério de aceite (CA-xx) vira um cenário em `features/NNN-<feature>.feature` com o mesmo ID no nome.
- Valores em R$ são inteiros em centavos. Datas usam `America/Sao_Paulo`.
- Segredos só no `.env`, que não vai para o Git e é bloqueado nas permissões (Read de `.env`, `.env.local` e `.env.production`, e `cat`/`head`/`tail`/`type` do `.env`). Para saber as variáveis, leia `.env.example`.
- Commit cita spec e critério. Cada critério passa por três commits:
  - `test(002): conferência sem divergência fecha o caixa (CA-01)`: só o teste, vermelho
  - `feat(002): fecha caixa sem divergência (CA-01)`: o mínimo para o verde
  - `refactor(002): <o que melhorou>`: sem mudar comportamento, tudo verde
- Teste de critério não se altera para passar. No verde e no refatorar, não edite, apague, pule (`@skip`, `@wip`) nem afrouxe cenário em `features/` ou teste em `tests/`. Se o teste parece errado, pare e proponha a mudança (na spec primeiro, se for de comportamento).
- Teste que fica vermelho durante um `refactor` indica mudança de comportamento: reverta a mudança em vez de ajustar o teste.
- Servidores MCP: nenhum instalado.

## Como você deve trabalhar
- Declare suas suposições. Se o pedido admite duas leituras, pergunte antes de escolher uma.
- O mínimo que resolve. Sem abstração de uso único, sem opção que ninguém pediu, sem tratar erro que não acontece.
- Toque só no necessário. Mantenha o estilo do arquivo e não refatore código que funciona e não faz parte do pedido.
- Diga como vai provar que funcionou, e rode a prova antes de dizer que terminou.
