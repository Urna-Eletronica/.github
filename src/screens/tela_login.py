import flet as ft
import sqlite3 as sql

class TelaLogin(ft.Container):
    def __init__(self, voto, adm, cadastro_callback):
        super().__init__()
        self.on_voto = voto
        self.on_adm = adm
        self.on_cadastro = cadastro_callback

        self.imagem_fundo = ft.Image(
            src="../assets/fundo.png",
            expand=True
        )

        self.imagem_logo = ft.Image(
            src="../assets/logo.png",
            width=150
        )

        cor_inputs = ft.Colors.with_opacity(0.49, ft.Colors.BLACK)

        self.email = ft.TextField(
            label="E-mail",
            prefix_icon=ft.Icons.EMAIL,
            width=500,
            height=50,
            border_radius=10,
            bgcolor=cor_inputs)

        self.senha = ft.TextField(
            label="Senha",
            password=True,
            prefix_icon=ft.Icons.LOCK,
            width=500,
            height=50,
            border_radius=10,
            bgcolor=cor_inputs)

        self.container_principal = ft.Container(
            content=ft.Column(
                controls=[
                    self.imagem_logo,
                    ft.Text("ACESSO À PLATAFORMA", size=24, weight="bold", color="#D6AB5F"),
                    ft.Text("Seja bem-vindo!", height=40),
                    self.email,
                    self.senha,
                    ft.ElevatedButton(text="Entrar", width=200, height=45, color="#D6AB5F", on_click=self.verificar),
                    ft.Row(
                        controls=[
                            ft.Text("Não tem uma conta?"),
                            ft.TextButton("Cadastre-se", on_click=self.go_cadastro)
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
            content=ft.Text("© 2025 Quarteto Music Awards. Todos os direitos reservados.", weight="bold"),
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
                    ],
                    expand=True
                )
            ],
            expand=True
        )

    def verificar(self, e):
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id_user, senha_user, cargo FROM dimUsuarios WHERE email_user = ?
            ''', (self.email.value,))

            resultado = cursor.fetchone()

            cursor.execute('''
                SELECT status FROM controleVotacao
            ''')

            votacao = cursor.fetchone()[0]

            if resultado:
                id_user, senha_bd, cargo = resultado
                if senha_bd == self.senha.value:
                    print("Login correto!")
                    if cargo == 'adm':
                        self.on_adm(id_user)
                    else:
                        if votacao == 'ativa':
                            self.on_voto(id_user)
                        else:
                            print('Votação não está disponivel no momento')
                else:
                    print("Senha incorreta!")
            else:
                print("Usuário não encontrado!")

            conn.close()
        except Exception as e:
            print("Erro:", e)

    def go_cadastro(self, e):
        self.on_cadastro()