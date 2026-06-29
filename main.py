# ==========================================================
# SISTEMA DE CONTROLEGERENCIAMENTO DE ESTOQUE
# Desenvolvido em Python + CustomTkinter + SQLite
# Desenvolvedor: Marco Antonio de Toledo Cardia - RA 85397
# ==========================================================

import sqlite3
import customtkinter as ctk

from tkinter import ttk
from tkinter import messagebox

# Aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Banco de Dados
conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS estoque(

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nota_fiscal TEXT NOT NULL,
    descricao_produto TEXT NOT NULL,
    quantidade INTEGER NOT NULL

)
""")

conn.commit()

# Layout do Sistema de Controle
janela = ctk.CTk()
janela.title("Sistema de Controle de Estoque")
janela.geometry("1100x650")
janela.resizable(False, False)

# Moldura Principal
frame = ctk.CTkFrame(
    janela,
    border_width=1,
    border_color="white",
    corner_radius=10
)

frame.pack(fill="both", expand=True, padx=15, pady=15)

# Título
titulo = ctk.CTkLabel(
    frame,
    text="CONTROLE DE ESTOQUE",
    font=("Arial",24,"bold")
)

titulo.pack(pady=20)

# Frame dos campos
frame_campos = ctk.CTkFrame(frame)
frame_campos.pack(fill="x", padx=20)

# Nota Fiscal
label_nf = ctk.CTkLabel(
    frame_campos,
    text="Nota Fiscal"
)

label_nf.grid(row=0,column=0,padx=10,pady=10)
entry_nf = ctk.CTkEntry(
    frame_campos,
    width=220
)

entry_nf.grid(row=1,column=0,padx=10)

# Descrição
label_desc = ctk.CTkLabel(
    frame_campos,
    text="Descrição"
)

label_desc.grid(row=0,column=1,padx=10)
entry_desc = ctk.CTkEntry(
    frame_campos,
    width=400
)

entry_desc.grid(row=1,column=1,padx=10)

# Quantidade
label_qtd = ctk.CTkLabel(
    frame_campos,
    text="Quantidade"
)

label_qtd.grid(row=0,column=2,padx=10)
entry_qtd = ctk.CTkEntry(
    frame_campos,
    width=120
)

entry_qtd.grid(row=1,column=2,padx=10)

# Frame Botôes
frame_botoes = ctk.CTkFrame(frame)
frame_botoes.pack(fill="x", padx=20, pady=20)

# Tabela
frame_tabela = ctk.CTkFrame(frame)
frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

colunas = (
    "ID",
    "Nota Fiscal",
    "Descrição",
    "Quantidade"
)

tabela = ttk.Treeview(
    frame_tabela,
    columns=colunas,
    show="headings",
    height=15
)

for coluna in colunas:
    tabela.heading(coluna,text=coluna)

tabela.column("ID",width=60,anchor="center")
tabela.column("Nota Fiscal",width=180)
tabela.column("Descrição",width=520)
tabela.column("Quantidade",width=120,anchor="center")

scroll = ttk.Scrollbar(
    frame_tabela,
    orient="vertical",
    command=tabela.yview
)

tabela.configure(
    yscrollcommand=scroll.set
)

tabela.pack(
    side="left",
    fill="both",
    expand=True
)

scroll.pack(
    side="right",
    fill="y"
)

# Funções
def limpar_campos():
    entry_nf.delete(0, "end")
    entry_desc.delete(0, "end")
    entry_qtd.delete(0, "end")
    entry_nf.focus()
    
# Atualizar Tabela 
def atualizar_tabela():

    for item in tabela.get_children():
        tabela.delete(item)

    cursor.execute("""
        SELECT *
        FROM estoque
        ORDER BY id
    """)

    produtos = cursor.fetchall()

    for produto in produtos:
        tabela.insert("", "end", values=produto)

# Adicionar Produto
def adicionar():

    nota = entry_nf.get().strip()
    descricao = entry_desc.get().strip()
    quantidade = entry_qtd.get().strip()

    if nota == "" or descricao == "" or quantidade == "":
        messagebox.showwarning(
            "Aviso",
            "Preencha todos os campos!"
        )
        return

    if not quantidade.isdigit():
        messagebox.showerror(
            "Erro",
            "Quantidade deve conter apenas números."
        )
        return

    cursor.execute("""
        INSERT INTO estoque
        (nota_fiscal, descricao_produto, quantidade)
        VALUES (?, ?, ?)
    """, (nota, descricao, int(quantidade)))

    conn.commit()

    atualizar_tabela()
    limpar_campos()

    messagebox.showinfo(
        "Sucesso",
        "Produto cadastrado com sucesso!"
    )
# Inserir Quantidade
def inserir_quantidade():

    selecionado = tabela.focus()

    if selecionado == "":
        messagebox.showwarning(
            "Aviso",
            "Selecione um produto."
        )
        return

    valores = tabela.item(selecionado, "values")
    id_produto = valores[0]
    quantidade = entry_qtd.get().strip()

    if quantidade == "":
        messagebox.showwarning(
            "Aviso",
            "Digite a quantidade."
        )
        return

    if not quantidade.isdigit():
        messagebox.showerror(
            "Erro",
            "Digite apenas números."
        )
        return

    cursor.execute("""
        SELECT quantidade
        FROM estoque
        WHERE id=?
    """, (id_produto,))

    atual = cursor.fetchone()[0]
    nova = atual + int(quantidade)

    cursor.execute("""
        UPDATE estoque
        SET quantidade=?
        WHERE id=?
    """, (nova, id_produto))

    conn.commit()

    atualizar_tabela()

    messagebox.showinfo(
        "Sucesso",
        "Quantidade atualizada!"
    )

# Excluir Produto
def excluir():
    selecionado = tabela.focus()

    if selecionado == "":
        messagebox.showwarning(
            "Aviso",
            "Selecione um produto."
        )
        return

    valores = tabela.item(selecionado, "values")

    resposta = messagebox.askyesno(
        "Excluir",
        f"Deseja excluir o produto\n\n{valores[2]}?"
    )

    if resposta:

        cursor.execute("""
            DELETE FROM estoque
            WHERE id=?
        """, (valores[0],))

        conn.commit()

        atualizar_tabela()

        messagebox.showinfo(
            "Sucesso",
            "Produto removido!"
        )

# Selecionar Linha
def selecionar(event):

    item = tabela.focus()

    if item == "":
        return

    dados = tabela.item(item, "values")

    limpar_campos()

    entry_nf.insert(0, dados[1])
    entry_desc.insert(0, dados[2])
    entry_qtd.insert(0, dados[3])

tabela.bind("<<TreeviewSelect>>", selecionar)

# Botôes
botao_adicionar = ctk.CTkButton(
    frame_botoes,
    text="Adicionar Produto",
    command=adicionar,
    width=180
)

botao_adicionar.pack(
    side="left",
    padx=10
)

botao_inserir = ctk.CTkButton(
    frame_botoes,
    text="Inserir Quantidade",
    command=inserir_quantidade,
    width=180
)

botao_inserir.pack(
    side="left",
    padx=10
)

botao_excluir = ctk.CTkButton(
    frame_botoes,
    text="Excluir Produto",
    command=excluir,
    width=180
)

botao_excluir.pack(
    side="left",
    padx=10
)

botao_atualizar = ctk.CTkButton(
    frame_botoes,
    text="Atualizar Lista",
    command=atualizar_tabela,
    width=180
)

botao_atualizar.pack(
    side="left",
    padx=10
)

# Botão Limpar
botao_limpar = ctk.CTkButton(
    frame_botoes,
    text="Limpar Campos",
    command=limpar_campos,
    width=180
)

botao_limpar.pack(
    side="left",
    padx=10
)

# Estilo da Tabela
style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass

style.configure(
    "Treeview",
    background="#2B2B2B",
    foreground="white",
    fieldbackground="#2B2B2B",
    rowheight=28,
    font=("Arial", 11)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 11, "bold")
)

# Carregar Dados ao Abrir 
atualizar_tabela()

# Fechar o Sistema
def fechar():

    conn.close()

    janela.destroy()

janela.protocol(
    "WM_DELETE_WINDOW",
    fechar
)

# Rodapé
rodape = ctk.CTkLabel(
    frame,
    text="Sistema de Controle de Estoque - Python | SQLite | CustomTkinter - V. 1.0"
    font=("Arial", 12)
)

rodape.pack(
    pady=10
)

# Executar
janela.mainloop()