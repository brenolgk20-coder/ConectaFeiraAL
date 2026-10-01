# ConectaFeira AL

Aplicação web acadêmica para divulgar feirinhas em Alagoas. O projeto começa com um escopo viável para o Projeto Integrador: contas de visitante/organizador, cadastro/edição/exclusão de feiras, catálogo público, filtros simples e mapa interativo.

## Requisitos

- Python 3.10 ou superior
- Acesso à internet no navegador para carregar os mapas e as fontes externas

## Como executar no Windows / VS Code

1. Extraia a pasta `ConectaFeiraAL` e abra essa pasta no VS Code.
2. No terminal integrado, crie e ative o ambiente virtual:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:

   ```powershell
   py -m pip install -r requirements.txt
   ```

4. Inicie o servidor:

   ```powershell
   uvicorn app.main:app --reload
   ```

5. Abra `http://127.0.0.1:8000` no navegador.

O banco SQLite `app/conectafeira.db` é criado automaticamente na primeira execução. Para cadastrar feiras, crie uma conta do tipo **Organizador**. Visitantes podem criar conta e consultar o catálogo.

## Fluxo principal

1. Criar uma conta como organizador.
2. Cadastrar uma feira e selecionar o ponto no mapa clicando nele.
3. Abrir **Minhas feiras** para editar ou excluir o cadastro.
4. Sair e consultar o catálogo público; usar os filtros de categoria, cidade/endereço e data.
5. Abrir os detalhes para ver horário, endereço e mapa.

## Escopo inicial

Incluído: autenticação básica, perfis simples por papel, gestão de feiras pelo próprio organizador, categorias, agenda de eventos futuros, filtros e mapas OpenStreetMap.

Fora deste primeiro corte: notificações e lembretes, avaliações/comentários, feedback de organizadores, anúncios patrocinados, chatbot de IA e painel avançado de moderação. Esses itens podem ser acrescentados se houver tempo e devem constar como não escopo no plano do projeto.

## Observações

- O mapa usa OpenStreetMap/Leaflet e requer internet para carregar os blocos cartográficos.
- A chave de sessão padrão serve apenas para desenvolvimento local. Antes de publicar, configure uma variável de ambiente `SESSION_SECRET` com uma chave longa e aleatória e use HTTPS.
- O projeto é um ponto de partida acadêmico. Antes de uma publicação real, acrescente proteção CSRF, recuperação de senha, validações adicionais e política de privacidade.

## Documentação do Projeto Integrador

A documentação acadêmica do projeto está em [`docs/Projeto_Integrador.md`](docs/Projeto_Integrador.md). Ela reúne a descrição do projeto, o escopo, os requisitos, os stakeholders, a metodologia, os riscos, o plano e as referências. Antes de enviar, confira se o texto e o cronograma correspondem ao trabalho realizado.
