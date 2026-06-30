# ==========================================================
# SISTEMA DE GERENCIAMENTOE DE ESTOQUE
# Desenvolvido em Python + CustomTkinter + SQLite
# Desenvolvedor: Marco Antonio de Toledo Cardia - RA 85397
# ==========================================================

import sqlite3                    # Banco de dados SQLite
import customtkinter as ctk       # Interface gráfica CustomTkinter
from tkinter import messagebox    # Caixas de mensagens

# ==========================================================
# CONFIGURAÇÃO DA APARÊNCIA DO SISTEMA
# ==========================================================

# Define o tema escuro da aplicação
ctk.set_appearance_mode("dark")

# Define o tema de cores azul
ctk.set_default_color_theme("blue")

# ==========================================================
# CONEXÃO COM O BANCO DE DADOS
# ==========================================================

# Cria (ou abre) o banco de dados usuarios.db
conn = sqlite3.connect("usuarios.db")

# Cursor responsável por executar comandos SQL
cursor = conn.cursor()

# ==========================================================
# CRIAÇÃO DA TABELA DE USUÁRIOS
# ==========================================================

# Caso a tabela ainda não exista, ela será criada
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

# Salva a alteração no banco
conn.commit()

# ==========================================================
# FUNÇÃO RESPONSÁVEL PELO LOGIN
# ==========================================================

def validar_login():

    # Obtém os valores digitados pelo usuário
    usuario = campo_usuario.get().strip()
    senha = campo_senha.get().strip()

    # Procura um usuário com login e senha informados
    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
        (usuario, senha)
    )

    resultado = cursor.fetchone()

    # Caso o usuário exista
    if resultado:

        # Exibe mensagem de sucesso
        resultado_login.configure(
            text="Login realizado com sucesso!",
            text_color="green"
        )

        # Fecha a janela de login
        app.destroy()

        # Importa a janela principal do sistema
        from main import SistemaEstoque

        # Abre o sistema
        sistema = SistemaEstoque()
        sistema.mainloop()

    # Caso login inválido
    else:

        resultado_login.configure(
            text="Usuário ou senha incorretos!",
            text_color="red"
        )

# ==========================================================
# JANELA DE CADASTRO DE USUÁRIO
# ==========================================================

def abrir_cadastro():

    # Cria uma nova janela
    janela = ctk.CTkToplevel(app)

    janela.title("Cadastro de Usuário")
    janela.geometry("420x380")
    janela.resizable(False, False)

    # ======================================================
    # MOLDURA PRINCIPAL
    # ======================================================

    frame = ctk.CTkFrame(
        master=janela,
        width=340,
        height=350,
        corner_radius=12,
        border_width=1,
        border_color="white"
    )

    frame.pack(pady=35)
    frame.pack_propagate(False)

    # ======================================================
    # TÍTULO
    # ======================================================

    ctk.CTkLabel(
        frame,
        text="Cadastro de Usuário",
        font=("Arial",22,"bold")
    ).pack(pady=(20,20))

    # ======================================================
    # CAMPO USUÁRIO
    # ======================================================

    ctk.CTkLabel(frame,text="Usuário").pack()

    campo_novo_usuario = ctk.CTkEntry(
        frame,
        width=250,
        placeholder_text="Digite o usuário"
    )

    campo_novo_usuario.pack(pady=(5,15))

    # ======================================================
    # CAMPO SENHA
    # ======================================================

    ctk.CTkLabel(frame,text="Senha").pack()

    campo_nova_senha = ctk.CTkEntry(
        frame,
        width=250,
        show="*",
        placeholder_text="Digite a senha"
    )

    campo_nova_senha.pack(pady=(5,25))

    # ======================================================
    # FUNÇÃO DE CADASTRO
    # ======================================================

    def cadastrar():

        # Obtém os valores digitados
        usuario = campo_novo_usuario.get().strip()
        senha = campo_nova_senha.get().strip()

        # Verifica se todos os campos foram preenchidos
        if usuario == "" or senha == "":

            messagebox.showwarning(
                "Aviso",
                "Preencha todos os campos!"
            )
            return

        try:

            # Insere o usuário no banco
            cursor.execute(
                "INSERT INTO usuarios(usuario, senha) VALUES (?, ?)",
                (usuario, senha)
            )

            conn.commit()

            messagebox.showinfo(
                "Sucesso",
                "Usuário cadastrado com sucesso!"
            )

            # Fecha a janela
            janela.destroy()

        # Caso o usuário já exista
        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Erro",
                "Este usuário já está cadastrado!"
            )

            janela.destroy()

    # ======================================================
    # BOTÃO CADASTRAR
    # ======================================================

    ctk.CTkButton(
        frame,
        text="Cadastrar",
        width=180,
        command=cadastrar
    ).pack()

    # ======================================================
    # BOTÃO LISTAR USUÁRIOS
    # ======================================================

    ctk.CTkButton(
        frame,
        text="Listar Usuários",
        width=180,
        command=abrir_lista_usuarios
    ).pack(pady=12)

# ==========================================================
# LISTAGEM DOS USUÁRIOS CADASTRADOS
# ==========================================================

def abrir_lista_usuarios():

    # Cria nova janela
    janela = ctk.CTkToplevel(app)
    janela.title("Lista de Usuários")
    janela.geometry("500x580")
    janela.resizable(False, False)

    # Moldura principal
    frame = ctk.CTkFrame(
        janela,
        width=460,
        height=500,
        corner_radius=12,
        border_width=1,
        border_color="white"
    )

    frame.pack(pady=20)
    frame.pack_propagate(False)

    # ======================================================
    # TÍTULO DA JANELA
    # ======================================================

    ctk.CTkLabel(
        frame,
        text="Lista de Usuários",
        font=("Arial",22,"bold")
    ).pack(pady=15)

    # ======================================================
    # CONSULTA AO BANCO
    # ======================================================

    cursor.execute("""
        SELECT id, usuario, senha 
        FROM usuarios
        ORDER BY usuario
    """)

    usuarios = cursor.fetchall()

    # Caso não exista usuário
    if not usuarios:

        ctk.CTkLabel(
            frame,
            text="Nenhum usuário cadastrado."
        ).pack()

    else:

        # Percorre todos os usuários encontrados
        for usuario in usuarios:

            ctk.CTkLabel(
                frame,
                text=f"ID: {usuario[0]}   Usuário: {usuario[1]}"
            ).pack(anchor="w", padx=15)
            

    frame.pack(pady=20)
    frame.pack_propagate(False)

    ctk.CTkLabel(
        frame,
        text="Informe o ID do usuário"
    ).pack()

    campo_id = ctk.CTkEntry(
        frame,
        width=150
        
    )
    campo_id.pack(pady=10)

    def excluir():

        id_usuario = campo_id.get().strip()

        if id_usuario == "":
            messagebox.showwarning(
                "Aviso",
                "Informe o ID."
            )
            return

        try:

            id_usuario = int(id_usuario)

        except ValueError:

            messagebox.showerror(
                "Erro",
                "ID inválido."
            )
            return

        # Verifica se existe
        cursor.execute(
            "SELECT * FROM usuarios WHERE id=?",
            (id_usuario,)
        )

        usuario = cursor.fetchone()

        if usuario is None:

            messagebox.showerror(
                "Erro",
                "Usuário não encontrado."
            )

            return

        # Confirma exclusão
        resposta = messagebox.askyesno(
            "Confirmação",
            f"Deseja realmente excluir o usuário '{usuario[1]}'?"
        )

        if resposta:

            cursor.execute(
                "DELETE FROM usuarios WHERE id=?",
                (id_usuario,)
            )

            conn.commit()

            messagebox.showinfo(
                "Sucesso",
                "Usuário excluído com sucesso!"
            )

            janela.destroy()

# ======================================================
# BOTÃO EXCLUIR
# ======================================================
  
    ctk.CTkButton(
        frame,
        text="Excluir",
        fg_color="#C62828",
        hover_color="#B71C1C",
        command=excluir
    ).pack(pady=100)

    # ======================================================
    # BOTÃO FECHAR
    # ======================================================
  
    ctk.CTkButton(
        frame,
        text="Fechar",
        command=janela.destroy
    ).pack(pady=20)
    
# ==========================================================
# JANELA PRINCIPAL (LOGIN)
# ==========================================================

# Cria a aplicação principal
app = ctk.CTk()

app.title("Sistema de Gerenciamento")
app.geometry("420x450")
app.resizable(False, False)

# Moldura principal
frame_login = ctk.CTkFrame(
    master=app,
    width=340,
    height=360,
    corner_radius=12,
    border_width=1,
    border_color="white"
)

frame_login.pack(pady=30)
frame_login.pack_propagate(False)

# Título da tela
ctk.CTkLabel(
    frame_login,
    text="Sistema de Login",
    font=("Arial",22,"bold")
).pack(pady=(25,20))

# Campo usuário
ctk.CTkLabel(frame_login,text="Usuário").pack()

campo_usuario = ctk.CTkEntry(
    frame_login,
    width=250,
    placeholder_text="Digite seu usuário"
)

campo_usuario.pack(pady=(5,15))

# Campo senha
ctk.CTkLabel(frame_login,text="Senha").pack()

campo_senha = ctk.CTkEntry(
    frame_login,
    width=250,
    show="*",
    placeholder_text="Digite sua senha"
)

campo_senha.pack(pady=(5,20))

# Botão Login
ctk.CTkButton(
    frame_login,
    text="Login",
    width=200,
    command=validar_login
).pack()

# Botão Cadastro
ctk.CTkButton(
    frame_login,
    text="Cadastrar Usuário",
    width=200,
    command=abrir_cadastro,
    fg_color="#D9D9D9",
    hover_color="#BFBFBF",
    text_color="black",
    corner_radius=8
).pack(pady=12)

# Label para exibir o resultado do login
resultado_login = ctk.CTkLabel(
    frame_login,
    text="",
    font=("Arial",14)
)

resultado_login.pack(pady=20)

# ==========================================================
# INICIA A APLICAÇÃO
# ==========================================================

app.mainloop()

# ==========================================================
# ENCERRA A CONEXÃO COM O BANCO
# ==========================================================

conn.close()