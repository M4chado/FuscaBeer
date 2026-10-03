# Better Harness Task-Loop Report

## At a Glance

- Loop Effectiveness: 54/100 (changes only after comparable later task outcomes)
- Asset Health / Repair Progress: 0/100 (0 verified, 0 partial, 1 pending)
- Demonstrated autonomy radius: not observed (not observed; not observed confidence)
- Strongest loop: Not enough evidence difference to name one.
- Largest observed leak: Use the priority moves; no single loop is uniquely weakest.
- Top expected gain: No priority benefit is available in this evidence boundary.

## What You Can Rely On Today

- No reliable user outcome has been demonstrated in this evidence boundary yet.

## What You Gain Next

- No priority Harness move is available in this evidence boundary.



### Why these moves matter

### Agente que segue a skill pode dar a tarefa por pronta sem a prova que o AGENTS.md exige
- Priority: Low · Evidence: not observed in this boundary
- Reason: Fato: o AGENTS.md exige `ruff check . && ruff format --check .`, `pytest` e `python manage.py behave` antes de todo commit, e o CLAUDE.md exige `pytest` e `python manage.py behave`. O passo 7 da skill criterio-para-teste define a prova completa como o cenário do CA, `pytest` e `ruff check .`, sem a checagem de formatação nem o behave completo. O hook de lint também roda só `ruff check`, no projeto inteiro e a cada Edit ou Write, enquanto o CLAUDE.md o descreve como a cada edição de `.py`. Inferência: quem seguir só a skill pode declarar o CA concluído sem rodar os outros cenários, e a falha de formatação só aparece depois. Incerteza: nenhuma sessão analisada tem edição, então o efeito não foi observado, e não há CI nem hook de commit que cubra a diferença.
- Expected Output:
  1. Dar ao próximo agente uma única definição de pronto, repetida de forma idêntica na skill, no AGENTS.md e no CLAUDE.md, e uma descrição do hook que corresponda ao script.

## Five Lifecycle Dimensions

| Dimension | What the evidence proves | Evidence boundary | Summary | Boundary / blocker |
| --- | --- | --- | --- | --- |
| Task Understanding | Not observed yet | not observed in this boundary | AGENTS.md, CLAUDE.md e a spec com RN e CA deixam o objetivo e o limite claros, mas nenhum episódio com mudança comprovou o uso. | not observed |
| Controlled Execution | Not observed yet | not observed in this boundary | Há passos de setup, permissões allow, ask e deny e um hook de lint, só lidos e não exercitados nas sessões analisadas. | not observed |
| Change Validation | Not observed yet | not observed in this boundary | Ruff, pytest e behave existem, mas a prova de pronto varia entre AGENTS.md, CLAUDE.md e a skill, e nenhuma checagem revisada e relevante foi observada. | not observed |
| Reliable Delivery | Not observed yet | not observed in this boundary | Não há aceitação nem recuperação observadas. O git push pede confirmação, mas nenhum gate mecânico garante a prova antes do commit. | not observed |
| Learning Capture | Not observed yet | not observed in this boundary | Existe uma skill de projeto, mas não há demanda repetida comprovada nem uso observado, então nada sustenta crédito adicional. | not observed |

## The 15 Small Checks

| Dimension | Small check | What the evidence proves | Evidence boundary |
| --- | --- | --- | --- |


## Evidence and Boundaries

- Episode coverage: 0 episodes, 0 edited, 0 closed, 0 repaired-and-passed
- Model: agent-work-loop-v4
- Session selection: not observed; 0 sessions analyzed of 0 eligible sessions; not observed confidence
- Delivery grades observed: not observed
- Source gaps: not observed
- Learning comparison: Not observed; 0 declared intervention(s)
