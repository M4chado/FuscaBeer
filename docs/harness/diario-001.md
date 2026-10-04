# Diário do agente — feature 001 (Registro de venda)

Harness: Claude Code com `AGENTS.md`, `CLAUDE.md`, skill `criterio-para-teste`, hook de lint e permissões de `.claude/settings.json`. Commits da feature: `2d72d27` (plano) a `fc37b00` (ajuste do harness).

## Nível do slider de autonomia

**Alto, com portão por tarefa.** Um pedido só (o PDF da atividade com "desenvolva o que se pede"); o agente escreveu o plano e executou T1 a T9 sem pedir aprovação entre as tarefas. O que segurou cada passo foi mecânico: cenário escrito antes e visto **falhando**, depois `ruff`, `pytest` e `behave` inteiros verdes antes de cada commit. Escolhemos esse nível porque a spec 001 já estava endurecida (20 CA executáveis, mensagens exatas, rotas e códigos de resposta), então o teste decidia quase tudo; o julgamento humano ficou para o plano, as suposições S-01 a S-08 e a revisão do diff.

O custo desse nível: **o plano não foi revisado pela equipe antes do código**, como pede o item 1 da atividade. O commit do plano veio antes do primeiro commit de código, mas na mesma sessão. A revisão está registrada no cabeçalho de `docs/specs/001-plano.md` como pendente. [equipe: registrar quem revisou e quando, e se alguma suposição muda]

## Uma vez em que o agente errou, e o que pegou o erro

**Pegou: teste.** O código de CA-02 gerado antes deste ciclo calculava o troco sem validar o valor recebido. Ao escrever o CA-05, o cenário falhou com **erro 500**: com R$ 17,99 o troco negativo só parou no `CHECK` da coluna `PositiveIntegerField`, e com o campo vazio deu `TypeError`. O CA-06 mostrou que o mesmo código aceitava valor recebido em Pix. Corrigido em `eaed975`.

**Pegou: nenhum mecanismo do harness (achado por acaso).** A migração `0001` tinha sido escrita à mão e não batia com os modelos (`id` sem `verbose_name`). Só apareceu quando o `makemigrations` da T2 gerou `AlterField` que ninguém pediu. Nenhum teste, hook ou revisão olhava isso. Virou mudança no harness (abaixo).

Erros menores pegos pelo `ruff` na prova: linhas acima de 100 colunas e import fora de ordem em quase toda tarefa. O hook `PostToolUse` não disparou nesta sessão; quem pegou foi o `ruff check` rodado na prova.

## Uma vez em que o agente perguntou antes de assumir (ou deveria)

**Deveria ter perguntado e não perguntou:** "a lista do dia mostra uma venda de R$ 20,00 em 'Pix' **com 2 itens**" (CA-01) admite duas leituras: 2 linhas ou 2 unidades. A compra tem 3 unidades (2 Chopp + 1 Água) em 2 linhas. O agente escolheu "linhas" (S-01), declarou no plano e seguiu sem perguntar, contra a regra do `AGENTS.md` ("se o pedido admite duas leituras, pergunte antes de escolher uma"). Declarar no plano só funciona se o plano for revisado antes do código, o que não aconteceu. As outras sete suposições também foram declaradas, e não perguntadas.

## O que mudaríamos no harness depois desta feature

| Mudança | Status |
|---|---|
| Uma única definição de pronto: os comandos de "Como testar" do `AGENTS.md`. A skill (passo 7) e o `CLAUDE.md` apontam para ela. Era o achado do `relatorio-2`, e se confirmou: a skill pedia só o cenário do CA, sem `ruff format --check` nem o `behave` completo | Feito em [fc37b00](https://github.com/M4chado/FuscaBeer/commit/fc37b00ceb8d4615f7be748323dcd1f96cc857bc) |
| `makemigrations --check --dry-run` na definição de pronto, para pegar migração fora de sincronia | Feito no mesmo commit |
| `CLAUDE.md` descreve o hook como ele é: `ruff check` no projeto a cada Edit/Write, sem formatar | Feito no mesmo commit |
| Hook ou regra que **pare** o agente quando houver suposição nova sem resposta da equipe. Hoje, a skill pede para perguntar, mas nada impede seguir | A fazer |
| A skill diz "não faça commit e não comece outro critério sem pedido", o que conflita com executar um plano de várias tarefas. Decidir se o plano revisado conta como pedido | A fazer |

## Critérios e restrições não atendidos

Os 20 CA passam e nenhum teste foi apagado, desativado ou ajustado para passar. Ficaram de fora como teste automatizado: **RS-01** (medida uma vez num navegador headless a 360 px: 6 toques para 3 itens no Pix, mas o sensor da spec é a cronometragem com o Gilmar), **RS-02** (script de carga com 5.000 vendas) e **RS-03** (checado com Playwright a 360 px, sem rolagem horizontal e alvos ≥ 44 px, mas sem teste no repositório). Nesta sessão, os testes rodaram em PostgreSQL 16 local, não no 17 do `docker-compose.yml`. [equipe: rodar o clone limpo com o Docker]
