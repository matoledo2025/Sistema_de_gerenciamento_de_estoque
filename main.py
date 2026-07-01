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

# Banco de Dados (SQLite)
conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()

# Tabelas em SQLite
cursor.execute("""
CREATE TABLE IF NOT EXISTS estoque(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nota_fiscal TEXT NOT NULL,
    descricao_produto TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    estoque_minimo INTEGER DEFAULT 5
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produto INTEGER,
    descricao TEXT,
    quantidade_vendida INTEGER,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Janela Principal (CustomTkinter)
janela = ctk.CTk()
janela.title("Controle de Estoque e Vendas")
janela.geometry("1150x700")
janela.resizable(False, False)

# Moldura Principal
frame = ctk.CTkFrame(janela, border_width=1, border_color="#3A3A3A", corner_radius=10)
frame.pack(fill="both", expand=True, padx=15, pady=15)

# Título
titulo = ctk.CTkLabel(frame, text="SISTEMA DE GERENCIAMENTO DE ESTOQUE", font=("Arial", 22, "bold"))
titulo.pack(pady=15)

# ----------------- FUNÇÕES DO SISTEMA -----------------

def limpar_campos():
    entry_id.configure(state="normal")
    entry_id.delete(0, "end")
    entry_id.insert(0, "Automático")
    entry_id.configure(state="disabled")
    entry_nf.delete(0, "end")
    entry_desc.delete(0, "end")
    entry_qtd.delete(0, "end")
    entry_minimo.delete(0, "end")
    entry_nf.focus()

def verificar_estoque_baixo():
    cursor.execute("SELECT descricao_produto, quantidade, estoque_minimo FROM estoque WHERE quantidade <= estoque_minimo")
    baixos = cursor.fetchall()
    if baixos:
        mensagem = "⚠️ ALERTA DE ESTOQUE BAIXO:\n\n"
        for prod, qtd, min_q in baixos:
            mensagem += f"• {prod} (Qtd: {qtd} / Mínimo: {min_q})\n"
        messagebox.showwarning("Aviso de Reposição", mensagem)

def atualizar_tabela(pesquisa=""):
    for item in tabela.get_children():
        tabela.delete(item)

    if pesquisa:
        cursor.execute("""
            SELECT id, nota_fiscal, descricao_produto, quantidade, estoque_minimo 
            FROM estoque 
            WHERE descricao_produto LIKE ? OR nota_fiscal LIKE ?
            ORDER BY id
        """, (f"%{pesquisa}%", f"%{pesquisa}%"))
    else:
        cursor.execute("SELECT id, nota_fiscal, descricao_produto, quantidade, estoque_minimo FROM estoque ORDER BY id")

    produtos = cursor.fetchall()
    for produto in produtos:
        tabela.insert("", "end", values=produto)

def limpar_pesquisa():
    entry_pesquisa.delete(0, "end")
    atualizar_tabela()

def buscar_produto(event=None):
    atualizar_tabela(entry_pesquisa.get().strip())

# Operações de Inserir (Create) e Editar (Update)
def adicionar_ou_atualizar():
    id_prod = entry_id.get()
    nota = entry_nf.get().strip()
    descricao = entry_desc.get().strip()
    quantidade = entry_qtd.get().strip()
    minimo = entry_minimo.get().strip()

    if nota == "" or descricao == "" or quantidade == "" or minimo == "":
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    if not quantidade.isdigit() or not minimo.isdigit():
        messagebox.showerror("Erro", "Os campos de quantidade e mínimo aceitam apenas números.")
        return

    if id_prod == "Automático":
        # CREATE
        cursor.execute("""
            INSERT INTO estoque (nota_fiscal, descricao_produto, quantidade, estoque_minimo)
            VALUES (?, ?, ?, ?)
        """, (nota, descricao, int(quantidade), int(minimo)))
        messagebox.showinfo("Sucesso", "Produto inserido com sucesso!")
    else:
        # UPDATE
        cursor.execute("""
            UPDATE estoque 
            SET nota_fiscal=?, descricao_produto=?, quantidade=?, estoque_minimo=?
            WHERE id=?
        """, (nota, descricao, int(quantidade), int(minimo), int(id_prod)))
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

    conn.commit()
    atualizar_tabela()
    limpar_campos()
    verificar_estoque_baixo()

# Registrar Venda (Abate quantidade e salva histórico)
def registrar_venda():
    selecionado = tabela.focus()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione o produto que deseja vender na tabela.")
        return

    valores = tabela.item(selecionado, "values")
    id_produto = valores[0]
    desc_produto = valores[2]
    qtd_atual = int(valores[3])
    
    qtd_venda = entry_qtd.get().strip()
    if not qtd_venda.isdigit() or int(qtd_venda) <= 0:
        messagebox.showerror("Erro", "Insira uma quantidade numérica válida para a venda.")
        return
    
    qtd_venda = int(qtd_venda)
    if qtd_venda > qtd_atual:
        messagebox.showerror("Erro", f"Estoque insuficiente! Quantidade atual: {qtd_atual}")
        return

    nova_qtd = qtd_atual - qtd_venda
    cursor.execute("UPDATE estoque SET quantidade=? WHERE id=?", (nova_qtd, id_produto))
    cursor.execute("INSERT INTO vendas (id_produto, descricao, quantidade_vendida) VALUES (?, ?, ?)", 
                   (id_produto, desc_produto, qtd_venda))
    
    conn.commit()
    atualizar_tabela()
    limpar_campos()
    messagebox.showinfo("Sucesso", f"Venda de {qtd_venda} unidades concluída!")
    verificar_estoque_baixo()

# Deletar (Delete)
def excluir():
    selecionado = tabela.focus()
    if selecionado == "":
        messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
        return

    valores = tabela.item(selecionado, "values")
    resposta = messagebox.askyesno("Excluir", f"Tem certeza que deseja apagar:\n\n{valores[2]}?")

    if resposta:
        cursor.execute("DELETE FROM estoque WHERE id=?", (valores[0],))
        conn.commit()
        atualizar_tabela()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")

# Selecionar Linha para campos (Read para edição)
def selecionar(event):
    item = tabela.focus()
    if item == "":
        return
    dados = tabela.item(item, "values")
    
    limpar_campos()
    entry_id.configure(state="normal")
    entry_id.delete(0, "end")
    entry_id.insert(0, dados[0])
    entry_id.configure(state="disabled")
    
    entry_nf.insert(0, dados[1])
    entry_desc.insert(0, dados[2])
    entry_qtd.insert(0, dados[3])
    entry_minimo.insert(0, dados[4])

# Janela de Relatório usando APENAS blocos do CustomTkinter
def abrir_relatorios_e_graficos():
    cursor.execute("SELECT descricao, SUM(quantidade_vendida) FROM vendas GROUP BY descricao ORDER BY SUM(quantidade_vendida) DESC LIMIT 5")
    dados_vendas = cursor.fetchall()
    
    if not dados_vendas:
        messagebox.showinfo("Relatório", "Nenhuma venda registrada no banco SQLite até o momento.")
        return
        
    janela_rep = ctk.CTkToplevel(janela)
    janela_rep.title("Gráfico Demonstrativo de Vendas")
    janela_rep.geometry("650x450")
    janela_rep.grab_set()
    
    lbl_title = ctk.CTkLabel(janela_rep, text="Top 5 - Produtos Mais Vendidos", font=("Arial", 16, "bold"))
    lbl_title.pack(pady=15)
    
    # Área do gráfico construída puramente com CustomTkinter Widgets
    frame_grafico = ctk.CTkFrame(janela_rep, fg_color="#1E1E1E", height=320, width=580)
    frame_grafico.pack(pady=10, padx=20, fill="both", expand=True)
    frame_grafico.pack_propagate(False)
    
    max_vendas = max([row[1] for row in dados_vendas]) if dados_vendas else 1
    
    # Exibir barras verticais usando CTkFrame
    for prod, qtd in dados_vendas:
        frame_coluna = ctk.CTkFrame(frame_grafico, fg_color="transparent")
        frame_coluna.pack(side="left", expand=True, fill="bottom", padx=10, pady=20)
        
        # Valor numérico da venda
        lbl_qtd = ctk.CTkLabel(frame_coluna, text=str(qtd), font=("Arial", 11, "bold"))
        lbl_qtd.pack(side="top", pady=2)
        
        # A barra propriamente dita (calculada proporcionalmente)
        altura_calculada = int((qtd / max_vendas) * 180) + 10
        barra = ctk.CTkFrame(frame_coluna, width=45, height=altura_calculada, fg_color="#1F6AA5", corner_radius=4)
        barra.pack(side="top")
        
        # Nome resumido do produto no eixo X
        nome_resumido = prod if len(prod) <= 10 else prod[:8] + ".."
        lbl_prod = ctk.CTkLabel(frame_coluna, text=nome_resumido, font=("Arial", 10), text_color="lightgray")
        lbl_prod.pack(side="top", pady=5)

# ----------------- Montando a Interface Gráfica do Projeto -----------------

# Formulário
frame_campos = ctk.CTkFrame(frame)
frame_campos.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(frame_campos, text="ID").grid(row=0, column=0, padx=10, pady=5)
entry_id = ctk.CTkEntry(frame_campos, width=90)
entry_id.insert(0, "Automático")
entry_id.configure(state="disabled")
entry_id.grid(row=1, column=0, padx=10)

ctk.CTkLabel(frame_campos, text="Nota Fiscal").grid(row=0, column=1, padx=10, pady=5)
entry_nf = ctk.CTkEntry(frame_campos, width=140)
entry_nf.grid(row=1, column=1, padx=10)

ctk.CTkLabel(frame_campos, text="Descrição do Produto").grid(row=0, column=2, padx=10, pady=5)
entry_desc = ctk.CTkEntry(frame_campos, width=320)
entry_desc.grid(row=1, column=2, padx=10)

ctk.CTkLabel(frame_campos, text="Quantidade").grid(row=0, column=3, padx=10, pady=5)
entry_qtd = ctk.CTkEntry(frame_campos, width=110)
entry_qtd.grid(row=1, column=3, padx=10)

ctk.CTkLabel(frame_campos, text="Estoque Mínimo").grid(row=0, column=4, padx=10, pady=5)
entry_minimo = ctk.CTkEntry(frame_campos, width=130)
entry_minimo.grid(row=1, column=4, padx=10)

# Barra de Pesquisa Integrada
frame_busca = ctk.CTkFrame(frame)
frame_busca.pack(fill="x", padx=20, pady=10)

entry_pesquisa = ctk.CTkEntry(frame_busca, placeholder_text="Pesquisar por descrição ou nota fiscal...", width=550)
entry_pesquisa.pack(side="left", padx=10, pady=8)
entry_pesquisa.bind("<KeyRelease>", buscar_produto)

botao_limpar_busca = ctk.CTkButton(frame_busca, text="Limpar Busca", command=limpar_pesquisa, width=120, fg_color="#555555", hover_color="#444444")
botao_limpar_busca.pack(side="left", padx=5)

# Visualização dos Dados  
frame_tabela = ctk.CTkFrame(frame)
frame_tabela.pack(fill="both", expand=True, padx=20, pady=5)

colunas = ("ID", "Nota Fiscal", "Descrição", "Estoque Atual", "Estoque Mínimo")
tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=11)

for coluna in colunas:
    tabela.heading(coluna, text=coluna)

tabela.column("ID", width=60, anchor="center")
tabela.column("Nota Fiscal", width=140)
tabela.column("Descrição", width=440)
tabela.column("Estoque Atual", width=120, anchor="center")
tabela.column("Estoque Mínimo", width=120, anchor="center")

scroll = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scroll.set)
tabela.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")
tabela.bind("<<TreeviewSelect>>", selecionar)

# Painel de Controle de Botões
frame_botoes = ctk.CTkFrame(frame)
frame_botoes.pack(fill="x", padx=20, pady=15)

btn_salvar = ctk.CTkButton(frame_botoes, text="Salvar / Atualizar", command=adicionar_ou_atualizar, width=150, fg_color="#2E7D32", hover_color="#1B5E20")
btn_salvar.pack(side="left", padx=8)

btn_venda = ctk.CTkButton(frame_botoes, text="Registrar Venda", command=registrar_venda, width=150, fg_color="#E65100", hover_color="#BF360C")
btn_venda.pack(side="left", padx=8)

btn_excluir = ctk.CTkButton(frame_botoes, text="Excluir Produto", command=excluir, width=140, fg_color="#C62828", hover_color="#B71C1C")
btn_excluir.pack(side="left", padx=8)

btn_grafico = ctk.CTkButton(frame_botoes, text="Gráfico de Vendas", command=abrir_relatorios_e_graficos, width=150, fg_color="#4A148C", hover_color="#311B92")
btn_grafico.pack(side="left", padx=8)

btn_limpar = ctk.CTkButton(frame_botoes, text="Limpar Campos", command=limpar_campos, width=140)
btn_limpar.pack(side="left", padx=8)

# Configuração de Estilos da Tabela
style = ttk.Style()
try:
    style.theme_use("clam")
except:
    pass
style.configure("Treeview", background="#2B2B2B", foreground="white", fieldbackground="#2B2B2B", rowheight=28, font=("Arial", 11))
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

# Inicialização do Banco de Dados na Interface
atualizar_tabela()
janela.after(800, verificar_estoque_baixo)

def fechar():
    conn.close()
    janela.destroy()

janela.protocol("WM_DELETE_WINDOW", fechar)

rodape = ctk.CTkLabel(frame, text="Sistema De Gerenciamento De Estoque - Versão 1.0 - RA 85397", font=("Arial", 11, "italic"), text_color="gray")
rodape.pack(pady=5)

janela.mainloop()