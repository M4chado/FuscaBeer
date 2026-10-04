@AGENTS.md

## Só para o Claude Code
- Abra o Claude Code com a `.venv` ativada, para que `python`, `pytest` e `ruff` sejam os do projeto.
- Use plan mode para qualquer tarefa que toque mais de 3 arquivos.
- Antes de dizer que terminou, rode os quatro comandos de "Como testar" do `AGENTS.md` e mostre a saída.
- O hook de lint roda `ruff check` no projeto inteiro depois de cada Edit ou Write (de qualquer arquivo). Ele não formata: rode `ruff format .` antes da prova. Se o hook apontar erro, corrija antes de seguir.
- `docs/specs/` é somente leitura: editar ali pede aprovação. Proponha a mudança em vez de editar.
- Use `/clear` ao trocar de tarefa, para a spec da tarefa anterior não ocupar contexto.
