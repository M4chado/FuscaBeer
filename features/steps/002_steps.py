import importlib

from behave import given, then, when

# Os passos da 001 viram ajudantes aqui. Reimportar não duplica os passos: o behave ignora
# o mesmo passo registrado de novo a partir do mesmo arquivo.
passos_001 = importlib.import_module("001_steps")
pagina = passos_001.pagina

# O relógio fica parado neste dia de operação durante o cenário (RN-11 da spec 001).
DIA_CORRENTE = "01/10/2026"
FORMAS = ("Dinheiro", "Débito", "Crédito", "Pix")


@given("que no dia de operação corrente o operador confirmou as vendas:")
def step_vendas_do_dia_corrente(context):
    context.vendas = []
    for minuto, linha in enumerate(context.table):
        momento = passos_001.em_brasilia(DIA_CORRENTE, f"20:{minuto:02d}")
        passos_001.acertar_relogio(context, momento)
        itens = passos_001.ler_itens_da_tabela(linha["itens"])
        context.vendas.append(passos_001.registrar_pela_tela(context, itens, linha["forma"]))


@given('que a venda em "{forma}" foi cancelada com o motivo "{motivo}"')
def step_venda_cancelada(context, forma, motivo):
    context.venda = next(v for v in context.vendas if v["forma"] == forma)
    passos_001.cancelar_pela_tela(context, motivo)
    assert context.resposta.status_code == 200, context.resposta.status_code


# ---------- Conferência (dirigida pela tela /caixa/) ----------


def linhas_da_conferencia(resposta):
    """Linhas da tabela de conferência como o conferente as lê: forma → esperado, contado
    e divergência."""
    return {
        linha.select_one("th").get_text(strip=True): {
            campo: linha.select_one(f".{campo}").get_text(" ", strip=True)
            for campo in ("esperado", "contado", "divergencia")
            if linha.select_one(f".{campo}")
        }
        for linha in pagina(resposta).select("#conferencia tbody tr")
    }


def conferir_pela_tela(context, contados):
    """Preenche o formulário da conferência, um valor contado por forma, na ordem de FORMAS."""
    tela = pagina(context.test.client.get("/caixa/"))
    formulario = tela.select_one("form.conferir")
    assert formulario, "a tela de conferência não oferece o formulário de valores contados"
    dados = {
        campo["name"]: campo.get("value", "") for campo in formulario.select("input[type=hidden]")
    }
    campos = formulario.select("input.contado")
    assert [c["data-forma"] for c in campos] == list(FORMAS), [c.get("data-forma") for c in campos]
    for campo, valor in zip(campos, contados, strict=True):
        dados[campo["name"]] = valor
    context.resposta = context.test.client.post(formulario["action"], dados, follow=True)


@when("o conferente abre a conferência do dia de operação corrente")
def step_abre_conferencia(context):
    context.resposta = context.test.client.get("/caixa/")
    assert context.resposta.status_code == 200, context.resposta.status_code


@then("a tela mostra os valores esperados:")
def step_valores_esperados(context):
    linhas = linhas_da_conferencia(context.resposta)
    esperados = {forma: campos.get("esperado") for forma, campos in linhas.items()}
    tabela = {linha["forma"]: f"R$ {linha['esperado']}" for linha in context.table}
    assert esperados == tabela, esperados


@when("o conferente informa os valores contados {dinheiro} / {debito} / {credito} / {pix}")
def step_informa_contados(context, dinheiro, debito, credito, pix):
    conferir_pela_tela(context, [dinheiro, debito, credito, pix])


@then('o caixa fica "{situacao}"')
def step_situacao_do_caixa(context, situacao):
    assert context.resposta.status_code == 200, context.resposta.status_code
    marcador = pagina(context.resposta).select_one(".situacao-caixa")
    assert marcador and marcador.get_text(strip=True) == situacao, marcador


@then("a tela não mostra divergência")
def step_sem_divergencia(context):
    linhas = linhas_da_conferencia(context.resposta)
    assert linhas, "a tela não mostra a tabela de conferência"
    divergencias = [c.get("divergencia", "") for c in linhas.values()]
    assert not any("Falta" in d or "Sobra" in d for d in divergencias), linhas
