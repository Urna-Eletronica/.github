import flet as ft
import sqlite3 as sql

class TelaCadastro(ft.Container):
    def __init__(self, login_callback):
        super().__init__()

        self.login_callback = login_callback

        self.nome = ft.TextField(
            label="Digite seu nome",
            width=300,
            height=50
        )

        self.cpf = ft.TextField(
            label="Digite seu cpf",
            width=300,
            height=50
        )

        self.email = ft.TextField(
            label="Digite seu email",
            width=300,
            height=50
        )

        self.senha = ft.TextField(
            label="Digite sua senha",
            password=True,
            width=300,
            height=50
        )

        self.confirmar = ft.ElevatedButton(
            text="confirmar",
            on_click=self.salvar1
        )
        
        self.login = ft.ElevatedButton(
            text="Já tem uma conta?",
            on_click=self.go_login
        )

        self.content = (
            ft.Column(
                controls=[self.nome,self.cpf,self.email,self.senha,self.confirmar,self.login]
            )
        )

    def salvar1(self, e):
        self.salvar(self.nome.value,self.cpf.value,self.email.value,self.senha.value)

    def salvar(self, nome, cpf, email, senha):
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO dimUsuarios (nome_user, cpf_user, email_user, senha_user, cargo)
                VALUES (?, ?, ?, ?, 'user')
            ''', (nome, cpf, email, senha))
            conn.commit()
            conn.close()
            print("Usuário salvo!")
        except sql.IntegrityError:
            print("Erro: CPF ou e-mail já cadastrado.")

    def go_login(self, e):
        self.login_callback()