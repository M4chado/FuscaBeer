#!/usr/bin/env bash
# Hook PostToolUse (Edit|Write): roda o ruff no projeto depois de cada edição.
# Sucesso: imprime "[hook ruff] OK". Falha: manda os erros para o Claude (exit 2).

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

# Usa o ruff do PATH (venv ativado) ou, se não houver, o da .venv do projeto.
if command -v ruff >/dev/null 2>&1; then
  RUFF=ruff
elif [ -x .venv/bin/ruff ]; then
  RUFF=.venv/bin/ruff
elif [ -x .venv/Scripts/ruff.exe ]; then
  RUFF=.venv/Scripts/ruff.exe
else
  echo "[hook ruff] ruff não encontrado. Ative a .venv e rode: pip install -r requirements.txt" >&2
  exit 1
fi

if saida=$("$RUFF" check --output-format concise . 2>&1); then
  echo "[hook ruff] OK"
  exit 0
fi

echo "[hook ruff] O lint falhou depois da edição. Corrija antes de seguir:" >&2
echo "$saida" >&2
exit 2
