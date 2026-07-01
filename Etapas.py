# FALTA AJUSTAR A JANELA DE LISTA DE USUÁRIO, A POSIÇÃO DOS BOTÕES
# CRIAR ASENHA MASTER E AJUSTA O USUÁRIO ADM
# NAJANELA CONTROLE DE ESTOQUE, ADICIONAR UM BOTÃO DE SAÍDA

# FLUXO GRAMA DO LOGIN E CADASTRO DE USUÁRIO

# Tela Login
#       │
#       ▼
# Cadastrar Usuário
#       │
#       ▼
# Autenticação do Administrador
#       │
#       ├── usuário comum
#       │        │
#       │        ▼
#       │   Acesso negado
#       │
#       ▼
# Administrador
#       │
#       ▼
# Cadastro de Usuário
#       │
#       ├── Usuário
#       ├── Senha
#       └── Perfil
#            ○ Funcionário
#            ○ Administrador


# Parte 1A – Banco de dados, criação da tabela e criação automática do primeiro administrador.
# Parte 1B – Login e controle do usuário logado.
# Parte 1C – Validação do administrador e permissões.
# Parte 2A – Cadastro de usuários (corrigido).
# Parte 2B – Listagem e exclusão de usuários.
# Parte 3A – Interface principal.
# Parte 3B – Inicialização do sistema e revisão final.