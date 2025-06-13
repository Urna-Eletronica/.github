import flet as ft
import sqlite3 as sql

class TelaLogin(ft.Container):
    def __init__(self, voto, adm, cadastro_callback):
        super().__init__()

        self.on_voto = voto
        self.on_adm = adm
        self.on_cadastro = cadastro_callback

        self.imagem_fundo = ft.Image(
            src="../assets/fundo_usuario.png",
        )

        self.imagem_logo = ft.Image(
            src=""
        )

        self.footer = ft.Container(
            bgcolor="#000000",
            opacity=0.44,
            content=ft.Text("© 2025 Quarteto Music Awards. Todos os direitos reservados.")
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
            content=ft.Column(
                controls=[
                    self.imagem_logo,
                    ft.Text("Seja bem-vindo"),
                    self.email,
                    self.senha,
                    self.confirmar,
                    self.cadastro
                ]
            )
        )

        self.content = (
            ft.Stack(
                controls=[
                    self.imagem_fundo,
                    self.container_principal
                ]
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
                        self.on_adm()
                    else:
                        self.on_voto()
                else:
                    print("Senha incorreta!")
            else:
                print("Usuário não encontrado!")

            conn.close()
        except Exception as e:
            print("Erro:", e)

    def go_cadastro(self, e):
        self.on_cadastro()


# import flet as ft
# import sqlite3 as sql

# class TelaLogin(ft.Container):
#     def __init__(self, voto_cb, adm_cb, cadastro_cb):
#         super().__init__(expand=True)

#         self.on_voto = voto_cb
#         self.on_adm = adm_cb
#         self.on_cadastro = cadastro_cb

#         # imagem de fundo que se expande
#         fundo = ft.Image(
#             src="assets/fundo_usuario.png",
#             fit=ft.ImageFit.COVER,
#             expand=True,    # << essencial para preencher tudo
#         )

#         # container central
#         login_box = ft.Container(
#             width=400,
#             padding=ft.padding.all(40),
#             bgcolor=Colors.BLACK,
#             opacity=0.6,
#             border_radius=15,
#             content=ft.Column(
#                 spacing=20,
#                 controls=[
#                     ft.Icon(ft.icons.ALBUM, size=48, color="#FFD700"),
#                     ft.Text("ACESSO DO ELEITOR",
#                             size=24,
#                             weight=ft.FontWeight.BOLD,
#                             color="#FFD700"),
#                     ft.Text("Seja bem‑vindo!", size=14, color="white"),
#                     ft.TextField(
#                         hint_text="E‑mail",
#                         prefix_icon=ft.icons.EMAIL,
#                         width=350,
#                         bgcolor=Colors.BLACK,
#                         opacity=0.7,
#                         color="white",
#                         border_radius=10,
#                     ),
#                     ft.TextField(
#                         hint_text="Senha",
#                         password=True,
#                         prefix_icon=ft.icons.LOCK,
#                         width=350,
#                         bgcolor=Colors.BLACK,
#                         opacity=0.7,
#                         color="white",
#                         border_radius=10,
#                     ),
#                     ft.ElevatedButton(
#                         text="Entrar",
#                         width=200,
#                         bgcolor="#FFD700",
#                         color="black",
#                         on_click=self.verificar
#                     ),
#                     ft.TextButton(
#                         text="Não tem uma conta? Clique aqui",
#                         on_click=self.go_cadastro,
#                         style=ft.ButtonStyle(color={"": "white"})
#                     ),
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 horizontal_alignment=ft.CrossAxisAlignment.CENTER
#             )
#         )

#         # footer
#         footer = ft.Container(
#             alignment=ft.alignment.bottom_center,
#             padding=ft.padding.all(12),
#             content=ft.Text(
#                 "© 2025 Quarteto Music Awards. Todos os direitos reservados.",
#                 size=10,
#                 color="white"
#             )
#         )

#         # empilha tudo
#         self.content = ft.Stack(
#             expand=True,   # << essencial para ocupar a tela inteira
#             controls=[
#                 fundo,
#                 # coluna que empurra o login_box pro centro
#                 ft.Column(
#                     expand=True,
#                     alignment=ft.MainAxisAlignment.CENTER,
#                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                     controls=[login_box]
#                 ),
#                 footer
#             ]
#         )

#     def verificar(self, e):
#         # aqui você pega os valores direto de self.email e self.senha,
#         # caso tenha guardado como atributo, ou então recupere de e.control.
#         pass

#     def go_cadastro(self, e):
#         self.on_cadastro()
