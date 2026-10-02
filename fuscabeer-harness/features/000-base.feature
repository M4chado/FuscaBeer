# language: pt
Funcionalidade: Base do projeto
  Confirma que o behave lê cenários em português e que a aplicação responde.
  Os cenários dos critérios de aceite da spec 001 entram em features/001-*.feature.

  Cenário: Painel administrativo exige login
    Dado que o visitante não tem sessão ativa
    Quando o visitante abre o endereço "/admin/"
    Então o sistema redireciona para a tela de login do painel
