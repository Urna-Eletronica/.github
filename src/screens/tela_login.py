import flet as ft
import sqlite3 as sql

class TelaLogin(ft.Container):
    def __init__(self, voto, adm, cadastro_callback):
        super().__init__()

        self.on_voto = voto
        self.on_adm = adm
        self.on_cadastro = cadastro_callback

        self.imagem_fundo = ft.Image(
            src="fundo_usuario.png",
        )

        self.imagem_logo = ft.Image(
            src=""
        )

        self.footer = ft.Container(
            bgcolor="#000000",
            opacity=0.44,
            text="© 2025 Quarteto Music Awards. Todos os direitos reservados."
        )

        self.email = ft.TextField(
            label="Digite seu email",
            width=300,
            height=50,
            bgcolor="#000000",
            opacity=0.49
        )

        self.senha = ft.TextField(
            label="Digite sua senha",
            password=True,
            width=300,
            height=50,
            bgcolor="#000000",
            opacity=0.49
        )

        self.confirmar = ft.ElevatedButton(
            text="Entrar",
            bgcolor="#000000",
            opacity=0.49,
            on_click=self.verificar
        )

        self.cadastro = ft.ElevatedButton(
            text="Não possui uma conta?",
            on_click=self.go_cadastro
        )

        self.container_principal = ft.Container(
            bgcolor = "#000000",
            opacity = 0.44,
            content = [self.imagem_logo, ft.Text("Seja bem-vindo"), self.email, self.senha, self.confirmar, self.cadastro],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.content = (
            ft.Stack(
                self.imagem_fundo,
                self.container_principal
            )
        )
    
    def verificar(self, e):
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT senha_user, cargo FROM dimUsuarios WHERE email_user = ?
            ''', (self.email.value,))

            resultado = cursor.fetchone()

            if resultado:
                senha_bd, cargo = resultado
                if senha_bd == self.senha.value:
                    print("Login correto!")

                    if cargo == 'adm':
                        self.on_adm()  # Chama callback do admin
                    else:
                        self.on_voto()  # Chama callback do voto

                else:
                    print("Senha incorreta!")
            else:
                print("Usuário não encontrado!")
            
            conn.close()
        except Exception as e:
            print("Erro:", e)

    def go_cadastro(self, e):
        self.on_cadastro()