# Achado escolhido no primeiro relatório

| | |
|---|---|
| **Relatório** | `relatorio-1.md` |
| **Dimensão** | Change Validation (Validação da mudança) |
| **Achado** | O lint pós-edição some em silêncio quando o ruff não é encontrado |
| **Por que este** | O hook de lint é o sensor que valida cada edição. Com `exit 1`, a falta do ruff virava erro não bloqueante e o agente seguia sem lint e sem saber. O reparo é de uma linha e pode ser provado na hora. |
| **Reparo aplicado** | O caminho "ruff não encontrado" de `.claude/hooks/lint.sh` passou de `exit 1` para `exit 2`, para o aviso chegar ao agente. |
| **Commit do reparo** | [f9574ad](https://github.com/M4chado/FuscaBeer/commit/f9574addc8926ca36bda002a7b1ac7ce3b90b845) |

**Prova:** depois do reparo, a edição do próprio `lint.sh` disparou o hook sem ruff disponível e a sessão recebeu `PostToolUse:Edit hook blocking error ... [hook ruff] ruff não encontrado. Ative a .venv e rode: pip install -r requirements.txt`. O script também devolveu `exit=2` quando rodado à mão sem ruff no PATH.
