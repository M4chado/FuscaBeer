# Better Harness Task-Loop Report

## At a Glance

- Loop Effectiveness: 50/100 (changes only after comparable later task outcomes)
- Asset Health / Repair Progress: 0/100 (0 verified, 0 partial, 4 pending)
- Demonstrated autonomy radius: not observed (not observed; not observed confidence)
- Strongest loop: Not enough evidence difference to name one.
- Largest observed leak: Use the priority moves; no single loop is uniquely weakest.
- Top expected gain: No priority benefit is available in this evidence boundary.

## What You Can Rely On Today

- No reliable user outcome has been demonstrated in this evidence boundary yet.

## What You Gain Next

- No priority Harness move is available in this evidence boundary.



### Why these moves matter

### O lint pós-edição some em silêncio quando o ruff não é encontrado
- Priority: Low · Evidence: not observed in this boundary
- Reason: Fato: em .claude/hooks/lint.sh o caminho 'ruff não encontrado' termina com exit 1, enquanto só o caminho de erro de lint termina com exit 2. Em hook PostToolUse, exit 1 é erro não bloqueante e a mensagem de orientação ('Ative a .venv...') tende a não chegar ao agente. CLAUDE.md promete que o hook roda a cada edição .py e pede correção de erros. Inferência: sem venv ativa nem .venv/Scripts/ruff.exe, a edição segue sem lint e o agente não percebe. Incerteza: o tratamento de exit 1 pelo Claude Code não foi observado em execução, e o ambiente do dono pode ter o ruff instalado.
- Expected Output:
  1. Uma edição .py sem ruff disponível devolve ao agente um aviso visível em vez de passar sem lint.

### O .env 'bloqueado nas permissões' só está bloqueado para a ferramenta Read
- Priority: Low · Evidence: not observed in this boundary
- Reason: Fato: AGENTS.md diz que o .env está bloqueado nas permissões, mas .claude/settings.json nega apenas Read(.env); não há regra para outros .env.* nem para leitura via Bash (por exemplo cat .env). Fato: o .env está no .gitignore. Inferência: a leitura por shell não passa pela regra de Read, então a garantia declarada é mais forte que a configurada. Incerteza: não foi testado em execução, e o .env local guarda senhas de desenvolvimento do Postgres, não segredos de produção.
- Expected Output:
  1. A proteção do .env descrita em AGENTS.md corresponde ao que as permissões realmente negam.

### O README do harness manda ler relatórios que não existem e o achado-1 está em branco
- Priority: Low · Evidence: not observed in this boundary
- Reason: Fato: docs/harness/README.md lista relatorio-1.md e relatorio-2.md, mas só README.md, achado-1.md e evidencias.md estão no repositório. Fato: docs/harness/achado-1.md ainda tem os campos entre colchetes (dimensão, achado, por que este, reparo, commit). Fato: o commit c494598 restaurou .claude e CLAUDE.md removidos por engano, então já houve perda de arquivos do harness. Inferência: o agente que seguir o README procura arquivos inexistentes e o ciclo medição → achado → reparo não é auditável. Incerteza: os relatórios podem estar sendo produzidos para a entrega da disciplina e ainda não commitados.
- Expected Output:
  1. Quem abrir docs/harness/ encontra todos os arquivos que o README cita e um achado preenchido com seu reparo.

### A regra 'passa antes de todo commit' não é aplicada por nada além do texto
- Priority: Low · Evidence: not observed in this boundary
- Reason: Fato: AGENTS.md exige ruff, pytest e behave verdes antes de todo commit, e CLAUDE.md exige mostrar a saída antes de dizer que terminou. Fato: não há .github nem workflow de CI, e .git/hooks só tem os exemplos padrão. Fato: a janela tem uma autorização de commit com exclusão de arquivos específicos, sem nenhuma verificação observada na mesma sessão. Inferência: hoje a validação antes do commit depende só de disciplina do agente e da pessoa. Incerteza: a sessão do commit teve turnos omitidos, o repositório é de uma disciplina e não tem app de domínio ainda, e nenhum merge ou entrega real foi aberto.
- Expected Output:
  1. Um commit com lint ou teste quebrado é recusado automaticamente, em vez de depender de lembrança.

## Five Lifecycle Dimensions

| Dimension | What the evidence proves | Evidence boundary | Summary | Boundary / blocker |
| --- | --- | --- | --- | --- |
| Task Understanding | Not observed yet | not observed in this boundary | AGENTS.md e CLAUDE.md dão stack, comandos, regras e a spec 001 como fonte da verdade; falta uso observado e o README do harness aponta para arquivos que não existem. | not observed |
| Controlled Execution | Not observed yet | not observed in this boundary | Há regras allow/ask/deny e o rascunho de comandos permitidos, mas a partida do ambiente não foi executada e a proteção do .env cobre só a ferramenta Read. | not observed |
| Change Validation | Not observed yet | not observed in this boundary | Existem ruff, pytest e behave, mas nenhuma validação foi observada nas sessões e o hook de lint falha sem bloquear quando o ruff não é encontrado. | not observed |
| Reliable Delivery | Not observed yet | not observed in this boundary | A regra 'passa antes de todo commit' só existe como texto: não há CI nem hook de pre-commit, e nenhuma aceitação foi observada. | not observed |
| Learning Capture | Not observed yet | not observed in this boundary | Há uma skill presente, mas as 6 sessões não formaram episódios comparáveis; não é possível dizer se há demanda repetida nem se a skill foi usada. | not observed |

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
