# ConectaFeira AL — Projeto Integrador

## 1. Sobre o projeto

O ConectaFeira AL é um site que estou desenvolvendo para reunir informações sobre feirinhas de Alagoas. A ideia é que quem organiza uma feira consiga divulgar os dados do evento e que os visitantes encontrem feiras por cidade, data, categoria e localização.

## 2. Por que escolhi esse tema

Escolhi esse tema porque as informações sobre feiras podem ficar espalhadas em vários lugares. Com o site, quero deixar mais fácil para as pessoas descobrirem o que está acontecendo perto delas e para os organizadores divulgarem seus eventos.

## 3. O que pretendo fazer

Meu objetivo é criar uma aplicação simples em que o organizador possa cadastrar e atualizar uma feira e o visitante consiga encontrar as informações principais, como data, horário, endereço e localização no mapa.

## 4. O que faz parte desta versão

Como estou fazendo o projeto sozinho e o prazo é curto, escolhi começar pelas funções principais:

- Criar conta como visitante ou organizador e entrar na conta.
- Cadastrar, consultar, editar e excluir as próprias feiras.
- Informar nome, descrição, categoria, data, horário, endereço, cidade e ponto no mapa.
- Consultar as próximas feiras em uma agenda pública.
- Filtrar as feiras por texto, categoria, cidade/endereço e data.
- Abrir os detalhes da feira e ver sua localização no mapa.
- Guardar os dados no banco SQLite.

### O que deixei para uma próxima versão

A proposta do professor traz outras ideias, mas decidi não incluir tudo nesta primeira versão. Ficaram para uma possível continuação:

- Notificações de feiras próximas e lembretes de eventos.
- Avaliações e comentários dos visitantes.
- Um espaço para os organizadores compartilharem experiências.
- Anúncios patrocinados.
- Conversa com um chatbot de inteligência artificial.
- Um painel completo para administração e moderação.
- Aplicativos para celular.

O professor explicou que eu poderia escolher um conjunto viável de requisitos. Por isso, deixei esse limite registrado no escopo.

## 5. Quem tem interesse no projeto

| Pessoa ou grupo | Participação no projeto |
|---|---|
| Eu, aluno desenvolvedor | Estou levantando os requisitos, desenvolvendo o sistema e preparando a documentação e a apresentação. |
| Professor orientador | Orienta o trabalho e avalia as entregas. |
| Organizadores de feiras | Podem divulgar e atualizar as informações dos eventos. |
| Visitantes e moradores | Podem procurar feiras e consultar os detalhes. |
| Administrador da plataforma | Poderia moderar o conteúdo em uma versão futura; essa função ainda não está incluída. |

## 6. Requisitos funcionais escolhidos

| Código | O que o sistema deve permitir | Situação |
|---|---|---|
| RF01 | Criar uma conta de visitante ou organizador. | Está no código; vou mostrar o fluxo na apresentação. |
| RF02 | Entrar e sair da conta. | Está no código; vou mostrar o fluxo na apresentação. |
| RF03 | Cadastrar uma feira com seus dados e localização. | Está no código; vou mostrar o fluxo na apresentação. |
| RF04 | Consultar, editar e excluir as próprias feiras. | Está no código; vou mostrar o fluxo na apresentação. |
| RF05 | Consultar feiras futuras e filtrar por texto, categoria, cidade/endereço e data. | Está no código; vou mostrar o fluxo na apresentação. |
| RF06 | Ver os detalhes da feira e sua posição no mapa quando houver coordenadas. | Está no código; o mapa precisa de internet para carregar. |

## 7. Requisitos não funcionais

| Código | Requisito | Como está no projeto |
|---|---|---|
| RNF01 | A navegação e os formulários devem ser fáceis de entender. | Fiz uma interface para computador e celular; vou conferir as telas antes de enviar o vídeo. |
| RNF02 | O site deve funcionar em navegadores atuais e poder ser iniciado localmente no Windows. | O projeto roda localmente com Python e as bibliotecas instaladas. |
| RNF03 | Os dados devem continuar salvos quando eu fechar e abrir o sistema. | Uso SQLite para guardar contas e feiras. |
| RNF04 | As senhas não devem ser guardadas como texto simples. | O código guarda um resumo criptográfico da senha. A chave de sessão padrão é apenas para uso local. |
| RNF05 | O visitante deve conseguir ver o mapa se tiver conexão com a internet. | O mapa usa Leaflet e OpenStreetMap, que precisam carregar recursos externos. |
| RNF06 | Antes de publicar o site na internet, devo reforçar a segurança. | Esta versão é para demonstração local. Ainda seriam necessárias medidas como HTTPS, uma chave de sessão própria e proteção CSRF. |

## 8. Como desenvolvi e quais tecnologias usei

Fui construindo o sistema por partes. Primeiro cuidei das contas e dos perfis; depois, do cadastro e gerenciamento das feiras; por último, da agenda, dos filtros e do mapa. Essa forma incremental me ajudou a concentrar o trabalho nas funções mais importantes para o prazo.

Usei Python com FastAPI para a aplicação, Jinja2 e HTML para montar as páginas, CSS para o visual, SQLAlchemy e SQLite para os dados, e Leaflet com OpenStreetMap para os mapas. Usei o Visual Studio Code para editar o projeto.

## 9. Riscos que considerei

| O que pode dar errado | Chance | Efeito | O que posso fazer |
|---|---|---|---|
| O Windows bloquear algum arquivo do Python ou de uma biblioteca. | Média | Alto | Usar o interpretador que funciona no computador e evitar dependências nativas que não sejam necessárias. Durante a configuração, já tive bloqueios desse tipo. |
| A internet não funcionar durante a apresentação e o mapa não carregar. | Média | Médio | Ter o endereço e a cidade preenchidos e preparar a demonstração com internet disponível. |
| Tentar fazer mais funções do que cabe no prazo. | Alta | Alto | Manter o foco nas contas, feiras, agenda, filtros e mapa; deixar as outras ideias como trabalho futuro. |
| Uma feira ficar sem coordenadas ou com o ponto errado. | Média | Médio | Conferir o ponto no mapa e os dados do endereço antes de gravar. |
| O banco de dados ser alterado ou perdido antes da apresentação. | Baixa | Alto | Fazer uma cópia de `app/conectafeira.db` e deixar uma feira fictícia preparada para a demonstração. |

## 10. Plano de trabalho

Este é um plano de referência para quatro semanas. Vou ajustar as etapas ao que realmente consegui fazer e às datas da disciplina.

| Período | O que planejei fazer |
|---|---|
| Semana 1 | Escolher o problema, definir o objetivo, os usuários, o escopo e os requisitos. |
| Semana 2 | Preparar as contas e as funções de cadastro, edição e exclusão de feiras. |
| Semana 3 | Montar a agenda pública, os filtros, os detalhes da feira e o mapa. |
| Semana 4 | Revisar o projeto, guardar capturas de tela, preencher o Connect e gravar o vídeo de apresentação. |

## 11. O que vou entregar

- O código do sistema e as instruções para executá-lo.
- Esta documentação com o escopo, os requisitos, os stakeholders, a metodologia, as tecnologias, os riscos e o plano de trabalho.
- Capturas de tela das partes principais: conta, cadastro da feira, edição, filtros, detalhes e mapa.
- O link do repositório ou do protótipo, conforme o que for pedido no Connect.
- As informações do projeto preenchidas individualmente no Connect: descrição, justificativa, bibliografia, metodologia, tecnologias e evidências do resultado.
- Um vídeo gravado por mim apresentando o projeto e mostrando o sistema, para enviar pelo canal indicado pelo professor.

Para a gravação, vou cadastrar uma feira fictícia com coordenadas válidas. Assim, a agenda e o mapa terão algo para mostrar. Também vou evitar deixar dados pessoais reais aparecendo na tela.

## 12. Resultado esperado

Com esta versão, quero mostrar que um organizador consegue cadastrar e manter uma feira e que um visitante consegue encontrá-la, usar os filtros e consultar sua localização. Por enquanto, o sistema é um projeto acadêmico que roda localmente; ainda não está preparado para ser publicado como um serviço comercial.

## Referências

FASTAPI. **Tutorial — User Guide**. [S. l.]: FastAPI, [s. d.]. Disponível em: <https://fastapi.tiangolo.com/tutorial/>. Acesso em: 30 set. 2026.

JINJA. **Jinja Documentation**. [S. l.]: Pallets Projects, [s. d.]. Disponível em: <https://jinja.palletsprojects.com/en/stable/>. Acesso em: 30 set. 2026.

LEAFLET. **Documentation: API reference**. [S. l.]: Leaflet, [s. d.]. Disponível em: <https://leafletjs.com/reference>. Acesso em: 30 set. 2026.

OPENSTREETMAP. **Copyright and License**. [S. l.]: OpenStreetMap Foundation, [s. d.]. Disponível em: <https://www.openstreetmap.org/copyright>. Acesso em: 30 set. 2026.

PYTHON SOFTWARE FOUNDATION. **Python 3 Documentation**. [S. l.]: Python Software Foundation, [s. d.]. Disponível em: <https://docs.python.org/3/>. Acesso em: 30 set. 2026.

SQLALCHEMY. **SQLAlchemy 2.0 Documentation**. [S. l.]: SQLAlchemy authors and contributors, 2026. Disponível em: <https://docs.sqlalchemy.org/en/20/>. Acesso em: 30 set. 2026.
