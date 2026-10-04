# Harness do Fusca Beer

Harness usado pela equipe: **Claude Code**.

| Arquivo | O que é |
|---|---|
| `relatorio-1.md` | Primeiro relatório do Better Harness, antes da configuração (LAB 3, Aula 08) |
| `achado-1.md` | O achado escolhido no primeiro relatório e o commit do reparo |
| `relatorio-2.md` | Segundo relatório, depois da configuração (LAB 3, Aula 09) |
| `evidencias.md` | Provas de que permissão, skill, hook e contexto funcionam, e a leitura da segunda medição |
| `diario-001.md` | Diário do agente na primeira feature (spec 001): autonomia, erros, perguntas e mudanças no harness |

## O que foi configurado

| Mecanismo | Onde | Dimensão do Agent Work Loop |
|---|---|---|
| Instruções | `AGENTS.md`, `CLAUDE.md` (importa o `AGENTS.md`) | Entendimento da tarefa |
| Permissões: 9 allow, 3 ask, 9 deny | `.claude/settings.json` | Entrega confiável |
| Skill `criterio-para-teste` | `.claude/skills/criterio-para-teste/` | Execução controlada · Captura de aprendizado |
| Hook `PostToolUse` com ruff | `.claude/settings.json` + `.claude/hooks/lint.sh` | Validação da mudança |

## Como gerar os relatórios

No Claude Code, na raiz do repositório:

```
/plugin marketplace add QoderAI/better-harness
/plugin install better-harness@better-harness
/better-harness
```

Salve a saída completa em `relatorio-1.md` (ou `relatorio-2.md`), sem editar.
