# ==========================================================
# SISTEMA DE GERENCIAMENTOE DE ESTOQUE
# Desenvolvido em Python + CustomTkinter + SQLite
# Desenvolvedor: Marco Antonio de Toledo Cardia - RA 85397
# ==========================================================

# Senha Master
# Usuário: admin
# Senha: admin123 com perfil Administrador).

import sqlite3                     
import customtkinter as ctk        
from tkinter import messagebox     

 # Configuração da Aparência do Sistema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Conexão com o Banco de Dados
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

# Criando a Tabela de Usuários
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    perfil TEXT NOT NULL DEFAULT 'Funcionario'
    )
    
    """)
conn.commit()

# Criando Usuário Master (PRIMEIRO ACESSO)
def criar_usuario_master():
    
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total = cursor.fetchone()[0]
    
# Se não houver nenhum usuário, cria o Administrador padrão
    if total == 0:
        cursor.execute("""
            INSERT INTO usuarios (usuario, senha, perfil)
            VALUES (?, ?, ?)
        """, ("admin", "admin123", "Administrador"))
        conn.commit()
        print("[INFO] Usuário master criado com sucesso! (admin / admin123)")

# Executa a verificação do usuário master
criar_usuario_master()

# Função do Login
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
        app.destroy()
        
# Verificar se o Login foi realizado com sucesso
        from main import SistemaEstoque
        sistema = SistemaEstoque()
        sistema.mainloop()
    else:
        resultado_login.configure(
            text="Usuário ou senha incorretos!",
            text_color="red"
        )
        
def validar_administrador():
    janela = ctk.CTkToplevel(app)
    janela.title("Autenticação do Administrador")
    janela.geometry("350x350")
    janela.resizable(False, False)
    janela.grab_set()
    
    ctk.CTkLabel(janela, text="Administrador", font=("Arial",20,"bold")).pack(pady=25)
    ctk.CTkLabel(janela, text="Usuário").pack()

    usuario_admin = ctk.CTkEntry(janela, width=220)
    usuario_admin.pack(pady=5)

    ctk.CTkLabel(janela, text="Senha").pack()
    senha_admin = ctk.CTkEntry(janela, show="*", width=220)
    senha_admin.pack(pady=5)
      

    def verificar():
        usuario = usuario_admin.get().strip()
        senha = senha_admin.get().strip()

        cursor.execute("""
            SELECT perfil FROM usuarios WHERE usuario=? AND senha=?
        """, (usuario, senha))
        
        resultado = cursor.fetchone()

        if resultado and resultado[0] == "Administrador":
            janela.destroy()
            abrir_cadastro()
        else:
            messagebox.showerror(
                "Acesso negado",
                "Somente administradores podem cadastrar usuários."
            )

    ctk.CTkButton(janela, text="Entrar", command=verificar).pack(pady=20)


# Layout de cadastro de usuários
def abrir_cadastro():
    janela = ctk.CTkToplevel(app)
    janela.title("Cadastro de Usuário")
    janela.geometry("420x420")
    janela.resizable(False, False)
    janela.grab_set()

    frame = ctk.CTkFrame(
        master=janela,
        width=360,
        height=380,
        corner_radius=12,
        border_width=1,
        border_color="white"
    )
    frame.pack(pady=20)
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Cadastro de Usuário", font=("Arial",22,"bold")).pack(pady=15)
    
    ctk.CTkLabel(frame, text="Usuário").pack()
    campo_novo_usuario = ctk.CTkEntry(frame, width=250, placeholder_text="Digite o usuário")
    campo_novo_usuario.pack(pady=5)

    ctk.CTkLabel(frame, text="Senha").pack()
    campo_nova_senha = ctk.CTkEntry(frame, width=250, show="*", placeholder_text="Digite a senha")
    campo_nova_senha.pack(pady=5)
    
    ctk.CTkLabel(frame, text="Perfil").pack(pady=(5,0))
    perfil = ctk.StringVar(value="Funcionario")
    
    ctk.CTkOptionMenu(
        frame,
        values=["Funcionario", "Administrador"],
        variable=perfil,
        width=250
    ).pack(pady=10)

    def cadastrar():
        usuario = campo_novo_usuario.get().strip()
        senha = campo_nova_senha.get().strip()
        perfil_selecionado = perfil.get()

        if usuario == "" or senha == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            cursor.execute(
                "INSERT INTO usuarios(usuario, senha, perfil) VALUES (?, ?, ?)",
                (usuario, senha, perfil_selecionado)
            )
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            janela.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este usuário já está cadastrado!")

    ctk.CTkButton(frame, text="Cadastrar", width=180, command=cadastrar).pack(pady=5)
    ctk.CTkButton(frame, text="Listar Usuários", width=180, command=abrir_lista_usuarios).pack(pady=5)

# Layout de listagem de usuários cadastrados
def abrir_lista_usuarios():
    janela = ctk.CTkToplevel(app)
    janela.title("Lista de Usuários")
    janela.geometry("500x600")
    janela.resizable(False, False)
    janela.grab_set()

    frame = ctk.CTkFrame(
        janela,
        width=460,
        height=560,
        corner_radius=12,
        border_width=1,
        border_color="white"
    )
    frame.pack(pady=20)
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Lista de Usuários", font=("Arial",22,"bold")).pack(pady=15)

    scroll_frame = ctk.CTkScrollableFrame(frame, width=420, height=200)
    scroll_frame.pack(pady=10)

    cursor.execute("SELECT id, usuario, perfil FROM usuarios ORDER BY usuario")
    usuarios = cursor.fetchall()

    if not usuarios:
        ctk.CTkLabel(scroll_frame, text="Nenhum usuário cadastrado.").pack()
    else:
        for usuario in usuarios:
            ctk.CTkLabel(
                scroll_frame,
                text=f"ID: {usuario[0]} | Usuário: {usuario[1]} | Perfil: {usuario[2]}"
            ).pack(anchor="w", padx=15, pady=2)
            
    ctk.CTkLabel(frame, text="Informe o ID do usuário para excluir").pack(pady=(10, 0))
    campo_id = ctk.CTkEntry(frame, width=150)
    campo_id.pack(pady=5)

    def excluir():
        id_usuario = campo_id.get().strip()

        if id_usuario == "":
            messagebox.showwarning("Aviso", "Informe o ID.")
            return

        try:
            id_usuario = int(id_usuario)
        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")
            return

        cursor.execute("SELECT * FROM usuarios WHERE id=?", (id_usuario,))
        usuario = cursor.fetchone()

        if usuario is None:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return

# Segurança: Impede que o usuário mestre 'admin' seja deletado acidentalmente
        if usuario[1] == "admin":
            messagebox.showerror("Erro", "O usuário master 'admin' não pode ser excluído por segurança.")
            return

        resposta = messagebox.askyesno(
            "Confirmação",
            f"Deseja realmente excluir o usuário '{usuario[1]}'?"
        )

        if resposta:
            cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
            janela.destroy()

    ctk.CTkButton(
        frame,
        text="Excluir",
        fg_color="#C62828",
        hover_color="#B71C1C",
        command=excluir
    ).pack(pady=10)

    ctk.CTkButton(frame, text="Fechar", command=janela.destroy).pack(pady=10)
    
# ==========================================================
# JANELA PRINCIPAL (LOGIN)
# ==========================================================

app = ctk.CTk()
app.title("Sistema de Gerenciamento")
app.geometry("420x480") 
app.resizable(False, False)

frame_login = ctk.CTkFrame(
    master=app,
    width=340,
    height=420, 
    corner_radius=12,
    border_width=1,
    border_color="white"
)
frame_login.pack(pady=30)
frame_login.pack_propagate(False)

ctk.CTkLabel(frame_login, text="Sistema de Login", font=("Arial",22,"bold")).pack(pady=(25,20))

ctk.CTkLabel(frame_login, text="Usuário").pack()
campo_usuario = ctk.CTkEntry(frame_login, width=250, placeholder_text="Digite seu usuário")
campo_usuario.pack(pady=(5,15))

ctk.CTkLabel(frame_login, text="Senha").pack()
campo_senha = ctk.CTkEntry(frame_login, show="*", width=250, placeholder_text="Digite sua senha")
campo_senha.pack(pady=(5,20))

ctk.CTkButton(frame_login, text="Login", width=200, command=validar_login).pack()

ctk.CTkButton(
    frame_login,
    text="Cadastrar Usuário",
    width=200,
    command=validar_administrador,
    fg_color="#D9D9D9",
    hover_color="#63eb72",
    text_color="black",
    corner_radius=8
).pack(pady=12)

# Texto de ajuda informativo para o primeiro acesso
ctk.CTkLabel(
    frame_login, 
    text="No primeiro acesso, use a Senha Master!", 
    font=("Arial", 11, "italic"),
    text_color="gray"
).pack(pady=5)

resultado_login = ctk.CTkLabel(frame_login, text="", font=("Arial",14))
resultado_login.pack(pady=5)

app.mainloop()

conn.close()