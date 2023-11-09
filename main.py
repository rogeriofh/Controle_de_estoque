import tkinter as tk
import tkinter.font as tkFont  # Importe a biblioteca tkinter.font
import sqlite3

janela_visualizacao = None


def adicionar_item():
    nome = nome_entry.get()
    quantidade = quantidade_entry.get()

    cursor.execute('INSERT INTO estoque (nome, quantidade) VALUES (?, ?)', (nome, quantidade))
    conn.commit()
    listar_itens()

    nome_entry.delete(0, tk.END)
    quantidade_entry.delete(0, tk.END)

def listar_itens():
    lista_itens.delete(0, tk.END)
    cursor.execute('SELECT * FROM estoque')
    for row in cursor.fetchall():
        lista_itens.insert(tk.END, f"{row[0]} - {row[1]}: {row[2]} unidades")

def abrir_janela_visualizacao():
    janela_visualizacao = tk.Toplevel(janela)
    janela_visualizacao.title("Visualização de Itens")

    # Defina o tamanho da janela visualização
    janela_visualizacao.geometry("600x400")  # Largura x Altura

    lista_itens_visualizacao = tk.Listbox(janela_visualizacao)
    lista_itens_visualizacao.pack(expand=True, fill="both")  # Ajusta o tamanho da lista de itens

    listar_itens_visualizacao(lista_itens_visualizacao)

    # Botão para excluir itens na segunda janela
    excluir_button = tk.Button(janela_visualizacao, text="Excluir Item Selecionado", command=lambda: excluir_item_visualizacao(lista_itens_visualizacao))
    excluir_button.pack()

    # Botão para editar um item selecionado
    editar_button = tk.Button(janela_visualizacao, text="Editar Item Selecionado", command=lambda: editar_item_visualizacao(lista_itens_visualizacao))
    editar_button.pack()

def excluir_item_visualizacao(lista):
    selecionado = lista.curselection()
    if selecionado:
        index = int(selecionado[0])
        item_id = int(lista.get(index).split('-')[0].strip())
        cursor.execute('DELETE FROM estoque WHERE id = ?', (item_id,))
        conn.commit()
        listar_itens_visualizacao(lista)

def listar_itens_visualizacao(lista):
    lista.delete(0, tk.END)
    cursor.execute('SELECT * FROM estoque')
    for row in cursor.fetchall():
        item_text = f"{row[0]} - {row[1]}: {row[2]} unidades"
        lista.insert(tk.END, item_text)

def editar_item_visualizacao(lista):
    selecionado = lista.curselection()
    if selecionado:
        index = int(selecionado[0])
        item_id = int(lista.get(index).split('-')[0].strip())
        cursor.execute('SELECT * FROM estoque WHERE id = ?', (item_id,))
        item = cursor.fetchone()

        editar_janela = tk.Toplevel(janela)
        editar_janela.title(f"Editar Item (ID: {item_id})")

        nome_label = tk.Label(editar_janela, text="Nome do Item:")
        nome_label.pack()
        nome_entry = tk.Entry(editar_janela)
        nome_entry.insert(0, item[1])
        nome_entry.pack()

        quantidade_label = tk.Label(editar_janela, text="Quantidade:")
        quantidade_label.pack()
        quantidade_entry = tk.Entry(editar_janela)
        quantidade_entry.insert(0, item[2])
        quantidade_entry.pack()

        salvar_button = tk.Button(editar_janela, text="Salvar", command=lambda: salvar_edicao(item_id, nome_entry.get(), quantidade_entry.get(), editar_janela))
        salvar_button.pack()

        # Defina a fonte dos botões
        fonte_botao = tkFont.Font(family="Helvetica", size=12)
        excluir_button['font'] = fonte_botao
        editar_button['font'] = fonte_botao

def salvar_edicao(item_id, novo_nome, nova_quantidade, janela_edicao):
    cursor.execute('UPDATE estoque SET nome=?, quantidade=? WHERE id=?', (novo_nome, nova_quantidade, item_id))
    conn.commit()
    janela_edicao.destroy()
    listar_itens_visualizacao(lista_itens_visualizacao)

def excluir_todos_itens():
    cursor.execute('DELETE FROM estoque')
    conn.commit()
    listar_itens()

def buscar_itens():
    termo = termo_busca.get()
    lista_itens.delete(0, tk.END)
    cursor.execute('SELECT * FROM estoque WHERE nome LIKE ?', ('%' + termo + '%',))
    for row in cursor.fetchall():
        lista_itens.insert(tk.END, f"{row[0]} - {row[1]}: {row[2]} unidades")
# Botão para iniciar a pesquisa
    buscar_button = tk.Button(janela, text="Buscar Itens", command=buscar_itens)
    buscar_button.pack(side="top", padx=10, pady=10, anchor="ne")

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL
    )
''')
conn.commit()

janela = tk.Tk()
janela.title("Controle de Estoque")

fonte = ("Helvetica", 14)
nome_label = tk.Label(janela, text="Nome do Item:")
nome_label.pack()
nome_entry = tk.Entry(janela, width=30)
nome_entry.pack(pady=5)


quantidade_label = tk.Label(janela, text="Quantidade:")
quantidade_label.pack()
quantidade_entry = tk.Entry(janela, width=30)
quantidade_entry.pack(pady=5)

# Campo de busca na janela principal
busca_label = tk.Label(janela, text="Pesquisar:")
busca_label.pack(side="top", padx=5, pady=5, anchor="ne")
busca_entry = tk.Entry(janela)
busca_entry.pack(side="top", padx=5, pady=5, anchor="ne")


adicionar_button = tk.Button(janela, text="Adicionar Item", command=adicionar_item, width=15, height=2)
adicionar_button.pack()

lista_itens = tk.Listbox(janela, width=100, height=20)
lista_itens.pack()

listar_button = tk.Button(janela, text="Listar Itens", command=listar_itens, width=15, height=2)
listar_button.pack()

visualizar_button = tk.Button(janela, text="Visualizar Itens", command=abrir_janela_visualizacao, width=15, height=2)
visualizar_button.pack()

excluir_todos_button = tk.Button(janela, text="Excluir Todos os Itens", command=excluir_todos_itens)
excluir_todos_button.pack(side="bottom", padx=10, pady=10, anchor="se")  # Ancora o botão no canto inferior direito


janela.geometry("800x600")


janela.mainloop()

conn.close()

