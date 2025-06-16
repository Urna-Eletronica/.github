import flet as ft
import sqlite3 as sql
from datetime import datetime

class TelaVotacao(ft.Container):
    def __init__(self, id_user):
        super().__init__()

        self.id_user = id_user

        self.todos_os_cards = []

        self.imagem_fundo = ft.Image(
            src="../assets/fundo.png",
            expand=True
        )

        self.pesquisar = ft.TextField(
            suffix_icon=ft.Icons.SEARCH,
            width=600,
            height=50,
            bgcolor=ft.Colors.with_opacity(0.49, ft.Colors.BLACK),
            border_radius=20,
            on_change=self.filtrar
        )

        self.lista_musicas = ft.Column(
            controls=[],
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )

        self.lista_musicas_scroll = ft.Container(
            content=self.lista_musicas,
            height=400,
            border_radius=10,
            padding=10
        )

        self.container_principal = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Text("Bem-vindo a sessão de votação", color="#D6AB5F", size=22),
                                        margin=ft.margin.only(left=20)
                                    ),
                                    ft.Divider(height=2, thickness=2, color="#D6AB5F"),
                                    ft.Container(
                                        content=ft.Text("Selecione logo abaixo sua música favorita", size=14),
                                        margin=ft.margin.only(left=20)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                expand=1
                            ),
                            ft.Image(src="../assets/logo.png", width=160)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        width=600
                    ),
                    self.pesquisar,
                    self.lista_musicas_scroll,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=30,
            bgcolor=ft.Colors.with_opacity(0.44, ft.Colors.BLACK),
            border_radius=20,
            width=700,
            height=600
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
                    ]
                )
            ]
        )

    def did_mount(self):
        self.carregar_musicas()
        print(self.id_user)
    
    def votar(self, e, id_musica):
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO factVotos (id_user, id_musica, data_voto)
                VALUES (?, ?, ?)
            ''', (self.id_user, id_musica, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            conn.commit()
            conn.close()
            print(f"Voto registrado para música ID {id_musica} pelo usuário {self.id_user}.")

        except sql.Error as err:
            print("Erro ao salvar voto:", err)

    def carregar_musicas(self):
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id_musica, nome_musica FROM dimMusicas
            ''')
            dados_musicas = cursor.fetchall()
            conn.commit()

            self.todos_os_cards.clear()

            for id_musica, nome_musica in dados_musicas:
                cursor.execute('''
                    SELECT nome_autor FROM dimAutores
                    WHERE id_autor IN (
                        SELECT id_autor FROM factAutorMusica WHERE id_musica = ?
                    )
                ''', (id_musica,))
                autores = [linha[0] for linha in cursor.fetchall()]
                texto_autores = ", ".join(autores)

                conn.commit()

                conteudo = ft.Row(
                    controls=[
                        ft.Image(src="a.png"),
                        ft.Column(
                            controls=[
                                ft.Text(nome_musica, color='#D6AB5F', size=18),
                                ft.Text(f"Artistas: {texto_autores}", color='#D6AB5F', size=12)
                            ],
                            expand=True
                        ),
                        ft.ElevatedButton(
                            text="Votar", bgcolor="#37323F", color="#D6AB5F",
                            on_click=lambda e, mid=id_musica: self.votar(e, mid)
                        )
                    ],
                )

                nova_musica = ft.Container(
                    content=conteudo,
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.49, ft.Colors.BLACK),
                    width=600,
                    border_radius=10
                )

                self.todos_os_cards.append((nome_musica.lower(), nova_musica))
                self.lista_musicas.controls.append(nova_musica)

            self.update()

            conn.close()

        except sql.Error as e:
            print("Erro ao carregar músicas:", e)

    def filtrar(self, e):
        filtro = self.pesquisar.value.strip().lower()

        for nome, card in self.todos_os_cards:
            card.visible = nome.startswith(filtro)

        self.update()