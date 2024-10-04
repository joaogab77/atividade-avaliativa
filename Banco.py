import sqlite3


def criar_tabela():
    conn = sqlite3.connect('time_futebol.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jogadores (
            numero INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            posicao TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()