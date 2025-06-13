import flet as ft
import sqlite3 as sql
from datetime import datetime

class TelaVotacao(ft.Container):
    def __init__(self, id_user):
        super().__init__()

        self.id_user = id_user

        self.todos_os_cards = []

        self.pesquisar = ft.TextField(
            label="Digite o nome da música",
            width=300,
            height=50,
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
            bgcolor="#1e1e1e",
            border_radius=10,
            padding=10
        )

        self.content = ft.Column(
            controls=[self.pesquisar, self.lista_musicas_scroll]
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
                conteudo = ft.ResponsiveRow(
                    controls=[
                        ft.Text(nome_musica, color='#D6AB5F'),
                        ft.ElevatedButton(
                            text="Votar",
                            on_click=lambda e, mid=id_musica: self.votar(e, mid)
                        )
                    ]
                )

                nova_musica = ft.Container(
                    content=conteudo,
                    padding=10,
                    bgcolor="#000000",
                    width=300
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