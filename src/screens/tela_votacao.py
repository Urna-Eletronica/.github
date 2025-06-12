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

        self.a = ft.ElevatedButton(
            text="a",
            on_click=self.carregar_musicas
        )

        self.musicas_disponiveis = []

        self.content = ft.Column(
            controls=[self.pesquisar, self.a]
        )

    def carregar_musicas(self, e):
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

                self.content.controls.insert(-1, nova_musica)
                self.update()

            conn.close()

        except sql.IntegrityError:
            print("Erro: CPF ou e-mail já cadastrado.")