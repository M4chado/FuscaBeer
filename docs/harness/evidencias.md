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

[resposta]

**Que dimensão não mudou, apesar de termos mexido nela? Por quê?**

[resposta — lembrem: existir não é o mesmo que ser usado]

**O que o relatório marcou como não observado? É ausência de fato, ou a ferramenta não tinha como ver?**

[resposta]
