import flet as ft
import sqlite3 as sql
from screens.tela_cadastro import TelaCadastro
from screens.tela_login import TelaLogin
from screens.tela_inicio_adm import TelaInicioAdm
from screens.tela_cadastro_m import TelaCadastroM

conn = sql.connect('urna.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# Cria a tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dimUsuarios(
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_user TEXT NOT NULL,
        cpf_user TEXT UNIQUE NOT NULL,
        email_user TEXT UNIQUE NOT NULL,
        senha_user TEXT NOT NULL,
        cargo TEXT NOT NULL CHECK(cargo IN ('adm', 'user'))
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS dimGeneros(
        id_genero INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_genero TEXT UNIQUE NOT NULL
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS dimMusicas(
        id_musica INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_musica TEXT NOT NULL,
        id_genero INTEGER NOT NULL,
        FOREIGN KEY(id_genero) REFERENCES dimGeneros(id_genero)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS dimAutores(
        id_autor INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_autor TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS factAutorMusica(
        id_relacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_autor INTEGER NOT NULL,
        id_musica INTEGER NOT NULL,
        FOREIGN KEY(id_autor) REFERENCES dimAutores(id_autor),
        FOREIGN KEY(id_musica) REFERENCES dimMusicas(id_musica)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS factVotos(
        id_voto INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER NOT NULL,
        id_musica INTEGER NOT NULL,
        data_voto TEXT NOT NULL,
        FOREIGN KEY(id_user) REFERENCES dimUsuarios(id_user),
        FOREIGN KEY(id_musica) REFERENCES dimMusicas(id_musica)
    )
''')

# Verifica se já existe um usuário com cargo 'adm'
cursor.execute('''
    SELECT COUNT(*) FROM dimUsuarios WHERE cargo = 'adm'
''')
existe_adm = cursor.fetchone()[0]

# Se não existir, insere o usuário adm padrão
if existe_adm == 0:
    cursor.execute('''
        INSERT INTO dimUsuarios (nome_user, cpf_user, email_user, senha_user, cargo)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Administrador', '123', 'adm@admin.com', 'admin', 'adm'))

conn.commit()
conn.close()

def main(page: ft.Page):
    page.title = "Sistema de Votação"

    def abrir_login():
        page.controls.clear()
        page.add(
            TelaLogin(
                abrir_voto,
                abrir_adm,
                abrir_cadastro
            )
        )

    def abrir_cadastro():
        page.controls.clear()
        page.add(TelaCadastro(abrir_login))

    def abrir_voto():
        page.controls.clear()
        page.add(ft.Text("Tela de Votação"))

    def abrir_adm():
        page.controls.clear()
        page.add(TelaInicioAdm(abrir_voto, abrir_cadastro_m))
    
    def abrir_cadastro_m():
        page.controls.clear()
        page.add(TelaCadastroM())

    # Inicia na tela de login
    abrir_login()

ft.app(target=main, view=ft.WEB_BROWSER)
