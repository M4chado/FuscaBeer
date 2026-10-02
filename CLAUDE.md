@AGENTS.md

## Só para o Claude Code
- Abra o Claude Code com a `.venv` ativada, para que `python`, `pytest` e `ruff` sejam os do projeto.
- Use plan mode para qualquer tarefa que toque mais de 3 arquivos.
- Antes de dizer que terminou, rode `pytest` e `python manage.py behave` e mostre a saída.
- O hook de lint roda sozinho a cada edição de `.py`. Se ele apontar erro, corrija antes de seguir.
- `docs/specs/` é somente leitura: editar ali pede aprovação. Proponha a mudança em vez de editar.
- Use `/clear` ao trocar de tarefa, para a spec da tarefa anterior não ocupar contexto.
