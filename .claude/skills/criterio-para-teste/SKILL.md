---
name: criterio-para-teste
description: Transforma um critério de aceite (CA-xx) de uma spec em docs/specs/ em cenário behave que falha primeiro e depois passa. Use quando pedirem para implementar, testar ou cobrir um CA ou uma regra RN-xx de uma spec, por exemplo "implementa o CA-02" ou "faz o troco em dinheiro funcionar".
---

# Do critério de aceite ao teste que passa

Um critério por vez. O texto do critério na spec é a fonte da verdade.

1. Abra a spec em `docs/specs/NNN-<feature>.md` e localize o critério pedido e as regras ligadas a ele na tabela de Rastreabilidade. Se o critério não existir, ou se o pedido admitir duas leituras, pare e pergunte.
2. Abra `features/NNN-<feature>.feature`. Se não existir, crie a partir de `modelo.feature` desta pasta e copie o bloco `Contexto` da spec.
3. Copie o cenário do critério da spec para o arquivo `.feature` sem mudar nenhuma palavra. O nome do cenário começa pelo ID (`Cenário: CA-02 ...`).
4. Procure em `features/steps/` os passos que já existem (`grep -rn "@given\|@when\|@then" features/steps`). Escreva só os que faltam, em `features/steps/NNN_steps.py`. Cada passo `Então` confere o que o usuário vê: código de resposta, texto da página ou redirecionamento. Nunca consulte o banco num `Então`.
5. Rode só esse cenário e confirme que ele **falha** pelo motivo esperado:
   `python manage.py behave features/NNN-<feature>.feature --name "CA-xx"`
   Se passar antes de existir implementação, o teste não testa nada: revise o passo antes de seguir.
6. Implemente o mínimo para o cenário passar. Se o critério depende de uma regra de cálculo (total, troco, totais do dia), escreva também o teste de unidade em `tests/test_<regra>.py`.
7. Rode a prova completa, que é a mesma do `AGENTS.md` ("Como testar"): `ruff check . && ruff format --check .`, `pytest`, `python manage.py behave` (todos os cenários, não só o do passo 5) e `python manage.py makemigrations --check --dry-run`.
8. **Pare.** Mostre a saída dos quatro comandos, liste os arquivos alterados e sugira a mensagem de commit no formato `feat(NNN): <o que mudou> (CA-xx)`. Não faça commit e não comece outro critério sem pedido.
