import tkinter as tk
from tkinter import messagebox
import sqlite3


def cadastrar_jogador():
    conn = sqlite3.connect('time_futebol.db')
    cursor = conn.cursor()

    numero = entry_numero.get()
    nome = entry_nome.get()
    posicao = entry_posicao.get()

    if numero == "" or nome == "" or posicao == "":
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return

    cursor.execute("SELECT * FROM jogadores WHERE numero = ?", (numero,))
    jogador = cursor.fetchone()

    if jogador:
        messagebox.showwarning("Erro", "Esse número já está cadastrado.")
    else:
        cursor.execute("INSERT INTO jogadores (numero, nome, posicao) VALUES (?, ?, ?)", (numero, nome, posicao))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Jogador {nome} cadastrado com sucesso!")

    conn.close()
    limpar_campos()


def alterar_jogador():
    conn = sqlite3.connect('time_futebol.db')
    cursor = conn.cursor()

    numero = entry_numero.get()
    nome = entry_nome.get()
    posicao = entry_posicao.get()

    cursor.execute("SELECT * FROM jogadores WHERE numero = ?", (numero,))
    jogador = cursor.fetchone()

    if jogador:
        cursor.execute("UPDATE jogadores SET nome = ?, posicao = ? WHERE numero = ?", (nome, posicao, numero))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Dados do jogador {nome} alterados com sucesso!")
    else:
        messagebox.showwarning("Erro", "Jogador não encontrado.")

    conn.close()
    limpar_campos()


def excluir_jogador():
    conn = sqlite3.connect('time_futebol.db')
    cursor = conn.cursor()

    numero = entry_numero.get()

    cursor.execute("SELECT * FROM jogadores WHERE numero = ?", (numero,))
    jogador = cursor.fetchone()

    if jogador:
        cursor.execute("DELETE FROM jogadores WHERE numero = ?", (numero,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Jogador excluído com sucesso!")
    else:
        messagebox.showwarning("Erro", "Jogador não encontrado.")

    conn.close()
    limpar_campos()


def consultar_jogador():
    conn = sqlite3.connect('time_futebol.db')
    cursor = conn.cursor()

    numero = entry_numero.get()

    cursor.execute("SELECT * FROM jogadores WHERE numero = ?", (numero,))
    jogador = cursor.fetchone()

    if jogador:
        entry_nome.delete(0, tk.END)
        entry_posicao.delete(0, tk.END)
        entry_nome.insert(0, jogador[1])
        entry_posicao.insert(0, jogador[2])
    else:
        messagebox.showwarning("Erro", "Jogador não encontrado.")

    conn.close()


# Função para listar todos os jogadores
def listar_jogadores():
    conn = sqlite3.connect('time_futebol.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jogadores")
    jogadores = cursor.fetchall()

    lista.delete(0, tk.END)  # Limpa a lista antes de preencher
    if jogadores:
        for jogador in jogadores:
            lista.insert(tk.END, f"Número: {jogador[0]}, Nome: {jogador[1]}, Posição: {jogador[2]}")
    else:
        lista.insert(tk.END, "Não há jogadores cadastrados.")

    conn.close()


# Função para limpar os campos de entrada
def limpar_campos():
    entry_numero.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_posicao.delete(0, tk.END)


# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Cadastro de Jogadores de Futebol")

# Widgets para o número, nome e posição dos jogadores
label_numero = tk.Label(root, text="Número:")
label_numero.grid(row=0, column=0, padx=10, pady=10)

entry_numero = tk.Entry(root)
entry_numero.grid(row=0, column=1, padx=10, pady=10)

label_nome = tk.Label(root, text="Nome:")
label_nome.grid(row=1, column=0, padx=10, pady=10)

entry_nome = tk.Entry(root)
entry_nome.grid(row=1, column=1, padx=10, pady=10)

label_posicao = tk.Label(root, text="Posição:")
label_posicao.grid(row=2, column=0, padx=10, pady=10)

entry_posicao = tk.Entry(root)
entry_posicao.grid(row=2, column=1, padx=10, pady=10)

# Botões para as operações de CRUD
btn_cadastrar = tk.Button(root, text="Cadastrar", command=cadastrar_jogador)
btn_cadastrar.grid(row=3, column=0, padx=10, pady=10)

btn_alterar = tk.Button(root, text="Alterar", command=alterar_jogador)
btn_alterar.grid(row=3, column=1, padx=10, pady=10)

btn_excluir = tk.Button(root, text="Excluir", command=excluir_jogador)
btn_excluir.grid(row=4, column=0, padx=10, pady=10)

btn_consultar = tk.Button(root, text="Consultar", command=consultar_jogador)
btn_consultar.grid(row=4, column=1, padx=10, pady=10)

btn_listar = tk.Button(root, text="Listar Jogadores", command=listar_jogadores)
btn_listar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Listbox para mostrar os jogadores cadastrados
lista = tk.Listbox(root, width=50, height=10)
lista.grid(row=6, column=0, columnspan=2, padx=10, pady=10)


# Iniciar o loop principal do Tkinter
root.mainloop()