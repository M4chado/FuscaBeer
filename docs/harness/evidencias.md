# Evidências do harness

Cole prints ou trechos copiados da sessão. Arquivo existir não prova que o mecanismo é usado.

## 1. Permissão: leitura do `.env` recusada

Pedido feito ao agente: `leia o arquivo .env e me mostre o conteúdo`

Regra que deveria recusar: `"deny": ["Read(.env)"]` em `.claude/settings.json`.

[cole aqui a resposta do Claude Code mostrando a recusa]

## 2. Skill: acionada sem ser citada

Sessão nova (`/clear`). Pedido feito sem citar a skill: `implementa o CA-02 da spec 001`

[cole aqui o trecho em que o agente carrega `criterio-para-teste`]

Reescritas da descrição até a skill ser acionada: [0, 1, 2…] — [o que mudou em cada reescrita]

## 3. Hook: lint disparado depois de uma edição

Pedido feito ao agente: `acrescente um import não usado em config/urls.py`

Saída esperada do hook: `[hook ruff] O lint falhou depois da edição` seguida do erro `F401`, e o agente corrigindo em seguida.

[cole aqui a saída do hook e a correção]

## 4. Contexto: `/context` numa sessão nova

[cole aqui a saída de `/context` antes de qualquer pedido]

---

## Leitura honesta da segunda medição

*Até meia página. Comparem `relatorio-1.md` com `relatorio-2.md`.*

**Que dimensão mudou, e com qual evidência?**

Os achados pendentes: de 4 no `relatorio-1.md` para 1 no `relatorio-2.md` (Asset Health continua 0/100, pois nenhum foi marcado como verificado). Os reparos que explicam a queda estão em commits: o hook que agora devolve `exit 2` quando falta o ruff (`f9574ad`), a proteção do `.env` estendida ao Bash (`fbd2188`) e os arquivos do `docs/harness/` que o README citava e não existiam. As dimensões mais tocadas foram Validação da mudança (hook de lint) e Execução controlada (allow/ask/deny). A Loop Effectiveness foi de 50 para 54, mas o próprio relatório diz que ela só muda com desfechos comparáveis. Então os 4 pontos não provam melhora: o que mudou de verdade foi a configuração, não o comportamento observado.

**Que dimensão não mudou, apesar de termos mexido nela? Por quê?**

Entrega confiável e Captura de aprendizado. Em Entrega confiável, "passa antes de todo commit" continua só como texto: não há CI nem hook de commit, e o relatório 2 ainda aponta que a definição de pronto aparece diferente na skill, no `AGENTS.md` e no `CLAUDE.md`. Em Captura de aprendizado, a skill `criterio-para-teste` existe, mas nenhum uso foi observado nas duas medições. Nas cinco dimensões a coluna "o que a evidência prova" ficou "Not observed yet" nos dois relatórios. O motivo é o lembrete da atividade: existir não é o mesmo que ser usado. Arquivo, regra e hook configurados não contam como prova até uma sessão mostrar o agente usando-os.

**O que o relatório marcou como não observado? É ausência de fato, ou a ferramenta não tinha como ver?**

Todas as cinco dimensões, o autonomy radius e os "Delivery grades" aparecem como "not observed", com 0 episódios e 0 sessões analisadas de 0 elegíveis, nos dois relatórios. Isso não é ausência de fato: o repositório tem mais de 20 commits e o `diario-001.md` registra o trabalho da feature 001. A ferramenta não tinha como ver, porque não encontrou sessões elegíveis (lacuna de fonte, não de trabalho). Por isso a segunda medição lê a configuração (o que está escrito), não o uso. Para a medição enxergar o uso, as provas da seção 4 precisam vir de sessões reais que o relatório consiga analisar.
