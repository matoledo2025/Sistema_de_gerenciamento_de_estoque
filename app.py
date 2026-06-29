# ==========================================================
# SISTEMA DE GERENCIAMENTO DE ESTOQUE
# Desenvolvido em Python + CustomTkinter + SQLite
# Desenvolvedor: Marco Antonio de Toledo Cardia - RA 85397
# ==========================================================

import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Configuração da aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Bando de dados_usuário
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

conn.commit()

# Funções
# Funções
def validar_login():
    usuario = campo_usuario.get().strip()
    senha = campo_senha.get().strip()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
        (usuario, senha)
    )

    resultado = cursor.fetchone()

    if resultado:
        resultado_login.configure(
            text="Login realizado com sucesso!",
            text_color="green"
        )

        # Fecha a janela de login
        app.destroy()

        # Abre o sistema de estoque
        from main import SistemaEstoque

        sistema = SistemaEstoque()
        sistema.mainloop()

    else:
        resultado_login.configure(
            text="Usuário ou senha incorretos!",
            text_color="red"
        )

def abrir_cadastro():

    janela = ctk.CTkToplevel(app)
    janela.title("Cadastro de Usuário")
    janela.geometry("420x380")
    janela.resizable(False, False)

 # Adicionando moldura
    frame = ctk.CTkFrame(
        master=janela,
        width=340,
        height=290,
        corner_radius=12,
        border_width=1,
        border_color="white"
    )

    frame.pack(pady=35)
    frame.pack_propagate(False)

    ctk.CTkLabel(
        frame,
        text="Cadastro de Usuário",
        font=("Arial", 22, "bold")
    ).pack(pady=(20, 20))

    ctk.CTkLabel(
        frame,
        text="Usuário"
    ).pack()

    campo_novo_usuario = ctk.CTkEntry(
        frame,
        width=250,
        placeholder_text="Digite o usuário"
    )
    campo_novo_usuario.pack(pady=(5, 15))

    ctk.CTkLabel(
        frame,
        text="Senha"
    ).pack()

    campo_nova_senha = ctk.CTkEntry(
        frame,
        width=250,
        show="*",
        placeholder_text="Digite a senha"
    )
    campo_nova_senha.pack(pady=(5, 25))

    def cadastrar():

        usuario = campo_novo_usuario.get().strip()
        senha = campo_nova_senha.get().strip()

        if usuario == "" or senha == "":
            messagebox.showwarning(
                "Aviso",
                "Preencha todos os campos!"
            )
            return

        try:

            cursor.execute(
                "INSERT INTO usuarios(usuario, senha) VALUES (?, ?)",
                (usuario, senha)
            )

            conn.commit()

            messagebox.showinfo(
                "Sucesso",
                "Usuário cadastrado com sucesso!"
            )

            janela.destroy()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Erro",
                "Este usuário já está cadastrado!"
            )

    ctk.CTkButton(
        frame,
        text="Cadastrar",
        width=180,
        command=cadastrar
    ).pack()


# Layout principal
app = ctk.CTk()
app.title("Sistema de Gerenciamento")
app.geometry("420x450")
app.resizable(False, False)

# Moldura branca
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

# Título
ctk.CTkLabel(
    frame_login,
    text="Sistema de Login",
    font=("Arial", 22, "bold")
).pack(pady=(25, 20))

# Usuário
ctk.CTkLabel(
    frame_login,
    text="Usuário"
).pack()

campo_usuario = ctk.CTkEntry(
    frame_login,
    width=250,
    placeholder_text="Digite seu usuário"
)

campo_usuario.pack(pady=(5, 15))

# Senha
ctk.CTkLabel(
    frame_login,
    text="Senha"
).pack()

campo_senha = ctk.CTkEntry(
    frame_login,
    width=250,
    show="*",
    placeholder_text="Digite sua senha"
)

campo_senha.pack(pady=(5, 20))

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

# Resultado
resultado_login = ctk.CTkLabel(
    frame_login,
    text="",
    font=("Arial", 14)
)

resultado_login.pack(pady=20)

# Execução
app.mainloop()

conn.close()