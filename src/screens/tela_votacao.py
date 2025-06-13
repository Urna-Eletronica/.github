import flet as ft
import sqlite3 as sql

class TelaVotacao(ft.Container):
    def __init__(self):
        super().__init__()

        self.pesquisar = ft.TextField(
            label="Digite o nome da música",
            width=300,
            height=50
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

    def carregar_musicas(self):
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT nome_musica FROM dimMusicas
            ''')
            nomes_m = [nome[0] for nome in cursor.fetchall()]
            print(nomes_m)

            conn.commit()

            for musica in nomes_m:
                nova_musica = ft.Container(
                    content=ft.Text(musica, color='#D6AB5F'),
                    padding=10,
                    bgcolor="#000000",
                    width=300
                )

                self.lista_musicas.controls.append(nova_musica)

            self.update()

            conn.close()

        except sql.Error as e:
            print("Erro ao carregar músicas:", e)