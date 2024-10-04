import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

# Função para conectar/criar o banco de dados
def conectar_banco():
    conexao = sqlite3.connect("times_futebol.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS times (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL,
            ano_fundacao INTEGER
        )
    """)
    conexao.commit()
    conexao.close()

# Função para adicionar um novo time ao banco de dados
def adicionar_time():
    time_id = entry_id.get()
    nome = entry_nome.get()
    cidade = entry_cidade.get()
    estado = entry_estado.get()
    ano_fundacao = entry_ano_fundacao.get()

    if time_id and nome and cidade and estado and ano_fundacao:
        try:
            conexao = sqlite3.connect("times_futebol.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO times (id, nome, cidade, estado, ano_fundacao) VALUES (?, ?, ?, ?, ?)
            """, (time_id, nome, cidade, estado, ano_fundacao))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Time cadastrado com sucesso!")
            limpar_campos()
            consultar_times()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar o time: {str(e)}")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")

# Função para alterar um time no banco de dados
def alterar_time():
    time_id = entry_id.get()
    nome = entry_nome.get()
    cidade = entry_cidade.get()
    estado = entry_estado.get()
    ano_fundacao = entry_ano_fundacao.get()

    if time_id and nome and cidade and estado and ano_fundacao:
        try:
            conexao = sqlite3.connect("times_futebol.db")
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE times
                SET nome = ?, cidade = ?, estado = ?, ano_fundacao = ?
                WHERE id = ?
            """, (nome, cidade, estado, ano_fundacao, time_id))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Time atualizado com sucesso!")
            limpar_campos()
            consultar_times()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar o time: {str(e)}")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")

# Função para excluir um time do banco de dados
def excluir_time():
    time_id = entry_id.get()
    if time_id:
        try:
            conexao = sqlite3.connect("times_futebol.db")
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM times WHERE id = ?", (time_id,))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Time excluído com sucesso!")
            limpar_campos()
            consultar_times()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir o time: {str(e)}")
    else:
        messagebox.showwarning("Atenção", "Preencha o ID do time para excluir!")

# Função para consultar times cadastrados no banco de dados
def consultar_times():
    for item in treeview.get_children():
        treeview.delete(item)

    conexao = sqlite3.connect("times_futebol.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM times")
    rows = cursor.fetchall()
    for row in rows:
        treeview.insert('', 'end', values=row)
    conexao.close()

# Função para preencher os campos de entrada ao selecionar um time
def preencher_campos(event):
    selected = treeview.selection()
    if selected:
        time_id, nome, cidade, estado, ano_fundacao = treeview.item(selected[0], 'values')
        entry_id.delete(0, END)
        entry_id.insert(0, time_id)
        entry_nome.delete(0, END)
        entry_nome.insert(0, nome)
        entry_cidade.delete(0, END)
        entry_cidade.insert(0, cidade)
        entry_estado.delete(0, END)
        entry_estado.insert(0, estado)
        entry_ano_fundacao.delete(0, END)
        entry_ano_fundacao.insert(0, ano_fundacao)

# Função para limpar os campos de entrada
def limpar_campos():
    entry_id.delete(0, END)
    entry_nome.delete(0, END)
    entry_cidade.delete(0, END)
    entry_estado.delete(0, END)
    entry_ano_fundacao.delete(0, END)

# Função para buscar times pelo nome
def buscar_time():
    nome_busca = entry_nome.get()

    if nome_busca:
        for item in treeview.get_children():
            treeview.delete(item)

        conexao = sqlite3.connect("times_futebol.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM times WHERE nome LIKE ?", ('%' + nome_busca + '%',))
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                treeview.insert('', 'end', values=row)
        else:
            messagebox.showinfo("Resultado", "Nenhum time encontrado com esse nome.")
        conexao.close()
    else:
        messagebox.showwarning("Atenção", "Digite o nome do time para buscar.")

# Configuração da interface
root = Tk()
root.title("Cadastro de Times de Futebol")

# Labels e campos de entrada
label_id = Label(root, text="ID do Time:")
label_id.grid(row=0, column=0, padx=10, pady=5)

entry_id = Entry(root)
entry_id.grid(row=0, column=1, padx=10, pady=5)

label_nome = Label(root, text="Nome do Time:")
label_nome.grid(row=1, column=0, padx=10, pady=5)

entry_nome = Entry(root)
entry_nome.grid(row=1, column=1, padx=10, pady=5)

label_cidade = Label(root, text="Cidade:")
label_cidade.grid(row=2, column=0, padx=10, pady=5)

entry_cidade = Entry(root)
entry_cidade.grid(row=2, column=1, padx=10, pady=5)

label_estado = Label(root, text="Estado:")
label_estado.grid(row=3, column=0, padx=10, pady=5)

entry_estado = Entry(root)
entry_estado.grid(row=3, column=1, padx=10, pady=5)

label_ano_fundacao = Label(root, text="Ano de Fundação:")
label_ano_fundacao.grid(row=4, column=0, padx=10, pady=5)

entry_ano_fundacao = Entry(root)
entry_ano_fundacao.grid(row=4, column=1, padx=10, pady=5)

# Botões
button_cadastrar = Button(root, text="Cadastrar Time", command=adicionar_time)
button_cadastrar.grid(row=5, column=0, padx=10, pady=10)

button_alterar = Button(root, text="Alterar Time", command=alterar_time)
button_alterar.grid(row=5, column=1, padx=10, pady=10)

button_excluir = Button(root, text="Excluir Time", command=excluir_time)
button_excluir.grid(row=6, column=0, padx=10, pady=10)

button_limpar = Button(root, text="Limpar Campos", command=limpar_campos)
button_limpar.grid(row=6, column=1, padx=10, pady=10)

button_buscar = Button(root, text="Buscar Time", command=buscar_time)
button_buscar.grid(row=7, column=0, padx=10, pady=10)

# Treeview para exibir os times cadastrados
treeview = ttk.Treeview(root, columns=("id", "nome", "cidade", "estado", "ano_fundacao"), show='headings')
treeview.heading("id", text="ID")
treeview.heading("nome", text="Nome")
treeview.heading("cidade", text="Cidade")
treeview.heading("estado", text="Estado")
treeview.heading("ano_fundacao", text="Ano de Fundação")
treeview.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Conectar o evento de seleção à função de preenchimento de campos
treeview.bind('<<TreeviewSelect>>', preencher_campos)

# Iniciar a conexão com o banco de dados e a interface
conectar_banco()
consultar_times()
root.mainloop()