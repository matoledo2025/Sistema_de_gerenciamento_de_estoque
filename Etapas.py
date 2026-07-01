# FALTA AJUSTAR A JANELA DE LISTA DE USUÁRIO, A POSIÇÃO DOS BOTÕES
# CRIAR ASENHA MASTER E AJUSTA O USUÁRIO ADM
# NAJANELA CONTROLE DE ESTOQUE, ADICIONAR UM BOTÃO DE SAÍDA

# FLUXO GRAMA DO LOGIN E CADASTRO DE USUÁRIO
            #         +---------------------------------+
            #         |       INÍCIO DO SISTEMA         |
            #         +---------------------------------+
            #                          |
            #                          v
            #         +---------------------------------+
            #         |   Verifica e Cria DB/Tabelas    |
            #         | (usuarios, estoque, vendas) e   |
            #         |   Usuário Master 'admin' se     |
            #         |        banco estiver vazio      |
            #         +---------------------------------+
            #                          |
            #                          v
            #         +---------------------------------+
            #         |     Abre Janela de Login        |
            #         +---------------------------------+
            #                    /           \
            #                   /             \
            #                  /               \
            #                 v                 v
            # [Botão Cadastrar Usuário]     [Botão Login]
            #                 |                 |
            #                 v                 v
            #    +-----------------------+  +-----------------------------------+
            #    | Pede Usuário/Senha do |  | Consulta DB se Usuário/Senha batem|
            #    |     Administrador     |  +-----------------------------------+
            #    +-----------------------+                    |
            #                |                                |
            #                v                               v
            #     /---------------------\          /---------------------\
            #    < É Administrador real? >        <  Credenciais Válidas? >
            #     \---------------------/          \---------------------/
            #             /       \                        /        \
            #         Não/         \Sim                 Sim/          \Não
            #           /           \                     /            \
            #          v             v                   v              v
            # +--------------+  +-----------------+ +--------------+ +---------------+
            # |Acesso Negado |  | Janela Cadastro | |Fecha Janela  | |Exibe mensagem |
            # |  (Bloqueia)  |  |   de Usuários   | |  de Login    | |  de Erro no   |
            # +--------------+  +-----------------+ +--------------+ |    Login      |
            #                           |                  |         +---------------+
            #                           v                  v
            #                  /-----------------\  +-------------------------------+
            #                 < Qual a ação aqui? > | Abre APP PRINCIPAL (Main)     |
            #                  \-----------------/  | SistemaEstoque()              |
            #                    /       |       \  +-------------------------------+
            #                   /        |        \                |
            #                  v         v         v               v
            #             +--------+ +---------+ +--------+ +-------------------------------+
            #             |Inserir | | Listar  | | Deletar| | Roda Verificação de Estoque  |
            #             | Novo   | | Usuários| | Usuário| | Baixo (Dispara Alerta na tela)|
            #             | Usuário| +---------+ |   ID   | +-------------------------------+
            #             +--------+             +--------+                |
            #                                                              |
            #                         +------------------------------------+
            #                         |
            #                         v
            #            /-------------------------------------------\
            #           <  Qual Operação o Usuário deseja realizar?   >
            #            \-------------------------------------------/
            #             /          |              |          \      \
            #            /           |              |           \      \
            #           v            v              v            v      v
            #   +---------+    +-----------+  +-----------+  +--------+ +-----------+
            #   | PESQUISA|    | ADICIONAR |  | SELECIONAR|  | EXCLUIR| | REGISTRAR |
            #   | PRODUTO |    | OU EDITAR |  | NA TABELA |  |PRODUTO | |   VENDA   |
            #   +---------+    +-----------+  +-----------+  +--------+ +-----------+
            #        |               |              |            |            |
            #        v               v              v            v            v
            # +------------+  /-------------\ +-----------+ /---------\ +-----------\
            # |Filtra SQL  | < ID=Automático?>|Preenche os| <Confirma?><Qtd_Venda <= >
            # |por texto   |  \-------------/ |campos de  |  \--------/ \Qtd_Atual? /
            # |na Treeview |    /         \   |texto com  |    /    \     \-------/
            # +------------+ Sim/           \Não os dados | Sim/     \Não   /     \
            #        |         /             \  da linha  |   /       \  Sim/      \Não
            #        |        v               v     |     v   v        v   v        v
            #        |  +-----------+ +-----------+ |  +---------+ +----+ +---+   +-------+
            #        |  |  INSERT   | |  UPDATE   | |  | DELETE  | |Can-| |SQL|   |Erro:  |
            #        |  | Novo Prod | | Prod Exist| |  | do Prod | |cela| |1. |   |Estoque|
            #        |  +-----------+ +-----------+ |  +---------+ +----+ |Abata| |Insufi-|
            #        |        |             |       |       |             |Qtd  | |ciente |
            #        |        v             v       |       v             |2.   | +-------+
            #        |  +-------------------------+ |  +---------+        |Salva|
            #        |  |    Commit no SQLite     | |  | Commit  |        |Venda|
            #        |  +-------------------------+ |  +---------+        +-----+
            #        |                |             |       |                |
            #        v                v             v       v                v
            # +---------------------------------------------------------------------+
            # |           Atualiza a Treeview (Lista Atualizada na Tela)            |
            # +---------------------------------------------------------------------+
            #                                 |
            #                                 v
            # +---------------------------------------------------------------------+
            # |           Roda Verificação de Estoque Baixo pós-alteração           |
            # |             (Se Estoque Atual <= Mínimo -> Emite Aviso)             |
            # +---------------------------------------------------------------------+
            #                                 |
            #                                 v
            # +---------------------------------------------------------------------+
            # |     [Botão Gráfico de Vendas] -> Abre Janela CTkToplevel e gera     |
            # |       Barras Visuais com CTkFrame baseado no Histórico do Banco     |
            # +---------------------------------------------------------------------+