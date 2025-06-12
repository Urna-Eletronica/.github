import flet as ft
import sqlite3 as sql

class TelaCadastroM(ft.Container):
    def __init__(self, voltar_callback):
        super().__init__()

        self.voltar_callback = voltar_callback

        self.voltar_btn = ft.ElevatedButton(
            text="Voltar",
            on_click=self.voltar
        )

        self.nome_m = ft.TextField(
            label="Digite o nome da música",
            width=300,
            height=50
        )

        self.autores = []

        self.autor = ft.TextField(
            label="Digite o nome do autor da música",
            width=300,
            height=50
        )

        self.autores.append(self.autor)

        self.novo_autor = ft.ElevatedButton(
            text="Adicionar novo autor",
            on_click=self.criar_input
        )

        self.tirar_input = ft.ElevatedButton(
            text="Tirar um autor",
            on_click=self.remover_input
        )

        self.genero = ft.TextField(
            label="Digite gênero da música",
            width=300,
            height=50
        )

        self.confirmar = ft.ElevatedButton(
            text="confirmar",
            on_click=self.salvar
        )

        self.content = (
            ft.Column(
                controls=[
                    self.voltar_btn,self.nome_m,self.autor,self.novo_autor,self.tirar_input,self.genero,self.confirmar
                    ]
            )
        )

    def criar_input(self, e):
        novo_input = ft.TextField(
            label="Digite o nome do autor da música",
            width=300,
            height=50
        )

        self.autores.append(novo_input)
        self.content.controls.insert(-4, novo_input)
        self.update()
        print(self.autores)

    def remover_input(self, e):
        if len(self.content.controls) > 6:  # Impede remover se houver só 1 autor
            del self.content.controls[-5]
            self.autores.pop()
            self.update()
        print(self.autores)
    def salvar(self, e):
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM dimMusicas WHERE nome_musica = ?
            ''', (self.nome_m.value.lower(),))
            existe_m = cursor.fetchone()

            if not existe_m:

                cursor.execute('''
                    SELECT * FROM dimGeneros WHERE nome_genero = ?
                ''', (self.genero.value.lower(),))
                existe_g = cursor.fetchone()

                if not existe_g:
                    cursor.execute('''
                        INSERT INTO dimGeneros(nome_genero)
                        VALUES(?)
                    ''', (self.genero.value.lower(),))
                    conn.commit()

                cursor.execute('''
                    SELECT id_genero FROM dimGeneros WHERE nome_genero = ?
                ''', (self.genero.value.lower(),))
                resultado = cursor.fetchone()[0]

                cursor.execute('''
                    INSERT INTO dimMusicas(nome_musica, id_genero)
                    VALUES(?,?)
                ''', (self.nome_m.value.lower(),resultado))

                conn.commit()

                cursor.execute('''
                    SELECT id_musica FROM dimMusicas WHERE nome_musica = ?
                ''', (self.nome_m.value,))

                idMusica = cursor.fetchone()[0]

                for autor in self.autores:
                    cursor.execute('''
                        SELECT * FROM dimAutores WHERE nome_autor = ?
                    ''', (autor.value.lower(),))
                    autor_existe = cursor.fetchone()

                    if not autor_existe:
                        cursor.execute('''
                            INSERT INTO dimAutores(nome_autor)
                            VALUES(?)
                        ''', (autor.value.lower(),))
                        conn.commit()

                    cursor.execute('''
                        SELECT id_autor FROM dimAutores WHERE nome_autor = ?
                    ''', (autor.value.lower(),))
                    idAutor = cursor.fetchone()[0]

                    cursor.execute('''
                        INSERT INTO factAutorMusica (id_autor, id_musica) VALUES (?, ?)
                    ''', (idAutor, idMusica))

                conn.commit()
                conn.close()
                print("Musica cadastrada!")

            else:
                print("Música já cadastrada")

        except sql.IntegrityError:
            print("Erro: CPF ou e-mail já cadastrado.")
        
    def voltar(self, e):
        self.voltar_callback()