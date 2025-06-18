import flet as ft
import sqlite3 as sql

class TelaCadastro(ft.Container):
    def __init__(self, login_callback):
        super().__init__()

        self.login_callback = login_callback

        self.imagem_fundo = ft.Image(
            src="fundo.png",
            expand=True
        )

        self.imagem_logo = ft.Image(
            src="logo.png",
            width=150
        )

        cor_inputs = ft.Colors.with_opacity(0.49, ft.Colors.BLACK)

        self.nome = ft.TextField(
            label="Digite seu nome",
            prefix_icon=ft.Icons.PERSON,
            width=500,
            height=50,
            border_radius=10,
            bgcolor=cor_inputs,
            color='#ffffff'
        )

        self.cpf = ft.TextField(
            label="Digite seu cpf",
            width=500,
            height=50,
            border_radius=10,
            bgcolor=cor_inputs,
            color='#ffffff'
        )

        self.email = ft.TextField(
            label="Digite seu email",
            prefix_icon=ft.Icons.EMAIL,
            width=500,
            height=50,
            border_radius=10,
            bgcolor=cor_inputs,
            color='#ffffff'
        )

        self.senha = ft.TextField(
            label="Digite sua senha",
            password=True,
            prefix_icon=ft.Icons.LOCK,
            width=500,
            height=50,
            border_radius=10,
            bgcolor=cor_inputs,
            color='#ffffff'
        )

        self.container_principal = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Crie a sua conta", size=24, weight="bold", color="#D6AB5F"),
                    ft.Text("Preencha seus dados logo abaixo", height=20, color='#ffffff'),
                    self.nome,
                    self.cpf,
                    self.email,
                    self.senha,
                    ft.ElevatedButton(text="Criar conta", width=200, height=45, color="#D6AB5F", on_click=self.salvar1),
                    ft.Row(
                        controls=[
                            ft.Text("Já tem uma conta?", color='#ffffff'),
                            ft.TextButton(text="Entrar", on_click=self.go_login),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            padding=20,
            bgcolor=ft.Colors.with_opacity(0.44, ft.Colors.BLACK),
            border_radius=20,
            width=600,
            height=500
        )

        self.footer = ft.Container(
            content=ft.Text("© 2025 Quarteto Music Awards. Todos os direitos reservados.", weight="bold", color='#ffffff'),
            padding=15,
            alignment=ft.alignment.center
        )

        self.content = ft.Stack(
            controls=[
                self.imagem_fundo,
                ft.Column(
                    controls=[
                        ft.Container(height=50),
                        ft.Row(
                            controls=[self.container_principal],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(height=10),
                        ft.Row(
                            controls=[self.footer],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                )
            ]
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