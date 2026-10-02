from behave import given, then, when


@given("que o visitante não tem sessão ativa")
def step_sem_sessao(context):
    context.test.client.logout()


@when('o visitante abre o endereço "{endereco}"')
def step_abre_endereco(context, endereco):
    context.resposta = context.test.client.get(endereco)


@then("o sistema redireciona para a tela de login do painel")
def step_redireciona_login(context):
    assert context.resposta.status_code == 302, context.resposta.status_code
    assert context.resposta["Location"].startswith("/admin/login/"), context.resposta["Location"]
