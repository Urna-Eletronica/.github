import flet as ft
import sqlite3 as sql
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class TelaInicioAdm(ft.Container):
    def __init__(self, votar_callback, cadastro_m_callback, id_user, sair_callback):
        super().__init__()

        self.sair_callback = sair_callback

        self.id_user = id_user

        self.cadastro_m_callback = cadastro_m_callback
        self.votar_callback = votar_callback

        self.todos_os_cards = []

        self.deslogar = ft.ElevatedButton(
            text='Sair',
            width=300,
            on_click=self.sair
        )

        self.imagem_fundo = ft.Image(
            src="fundo_pb.png",
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
                            ft.ElevatedButton(
                                text="Iniciar Votação",
                                on_click = self.iniciar_votacao
                            ),
                            ft.ElevatedButton(
                                text="Votar",
                                on_click = self.abrir_votacao
                            ),
                            ft.ElevatedButton(
                                text="Encerrar Votação",
                                on_click = self.encerrar_votacao
                            )
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

        self.cadastro_m = ft.ElevatedButton(
            text="Cadastrar Músicas",
            on_click=self.abrir_cadastro_m
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
                        self.deslogar,
                        ft.Container(height=50),
                        ft.Row(
                            controls=[self.container_principal],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER 
                        ),
                        ft.Container(height=2),
                        ft.Row(
                            controls=[self.cadastro_m],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(height=5),
                        ft.Row(
                            controls=[self.footer],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                )
            ],
            expand=True,
        )


    def did_mount(self):
        self.carregar_musicas()
        print(self.id_user)

    def abrir_votacao(self, e):
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT status FROM controleVotacao
            ''')
            resultado = cursor.fetchone()[0]

            if resultado == 'ativa':
                self.votar_callback(self.id_user)

            else:
                print('Votação não está aberta!')

        except Exception as err:
            print("Erro ao iniciar votação:", err)


    def abrir_cadastro_m(self, e):
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT status FROM controleVotacao
            ''')
            resultado = cursor.fetchone()[0]

            if resultado == 'inativa':
                self.cadastro_m_callback(self.id_user)
            else:
                print('A votação está ativa, não tem como adicionar uma nova música')
        
        except Exception as err:
            print("Erro ao cadastrar música:", err)

    # FUNÇÃO PARA INICIAR A VOTAÇÃO
    
    def iniciar_votacao(self, e):
        os.makedirs("imagens_musicas", exist_ok=True)
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT status FROM controleVotacao
            ''')
            resultado = cursor.fetchone()

            if resultado:
                self.votacao_ativa = True if resultado[0] == 'ativa' else False

            if not self.votacao_ativa:

                cursor.execute('''
                    UPDATE controleVotacao SET status = 'ativa' WHERE id = 1
                ''')
                conn.commit()
                conn.close()
                print("Votação iniciada e salva no banco!")
                os.remove('resultados/resultado_votacao.pdf')
            
            else:
                print('Já existe uma votação em andamento!')

        except Exception as err:
            print("Erro ao iniciar votação:", err)

    # FUNÇÃO PARA FINALIZAR A VOTAÇÃO

    def encerrar_votacao(self, e):
        os.makedirs("imagens_musicas", exist_ok=True)
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT status FROM controleVotacao
            ''')
            resultado = cursor.fetchone()

            cursor.execute('''
                SELECT dimMusicas.nome_musica, COUNT(factVotos.id_voto) AS total_votos
                FROM factVotos
                INNER JOIN dimMusicas ON factVotos.id_musica = dimMusicas.id_musica
                GROUP BY dimMusicas.id_musica
                ORDER BY total_votos DESC
            ''')

            resultado_votacao = cursor.fetchall()

            if resultado:
                self.votacao_ativa = True if resultado[0] == 'ativa' else False

            if self.votacao_ativa:
                cursor.execute('''
                    UPDATE controleVotacao SET status = 'inativa' WHERE id = 1
                ''')
                conn.commit()
                print("Votação encerrada e salva no banco!")
                os.makedirs("resultados", exist_ok=True)

                pdf_path = os.path.join("resultados", "resultado_votacao.pdf")
                c = canvas.Canvas(pdf_path, pagesize=A4)
                largura, altura = A4

                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, altura - 50, "Resultado Final da Votação")

                c.setFont("Helvetica", 12)
                y = altura - 100

                if resultado_votacao:
                    for nome_musica, total_votos in resultado_votacao:
                        c.drawString(50, y, f"{nome_musica} - {total_votos} voto(s)")
                        y -= 20
                        if y < 50:
                            c.showPage()
                            y = altura - 50
                else:
                    c.drawString(50, y, "Nenhum voto registrado.")

                c.save()
                os.startfile(pdf_path)

                print(f"PDF de resultado salvo em: {pdf_path}")

                cursor.execute('DELETE FROM factVotos')
                cursor.execute('DELETE FROM factAutorMusica')
                cursor.execute('DELETE FROM dimMusicas')

                imagens_dir = "imagens_musicas"
                for arquivo in os.listdir(imagens_dir):
                    caminho = os.path.join(imagens_dir, arquivo)
                    if os.path.isfile(caminho):
                        os.remove(caminho)
                print("Imagens antigas removidas!")

                conn.commit()
            
            else:
                print('Nenhuma votação em andamento!')

            self.lista_musicas.controls.clear()
            self.todos_os_cards.clear()
            self.update()

        except Exception as err:
            print("Erro ao encerrar votação:", err)

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

                imagem = ft.Image(
                    src=f'imagens_musicas/{id_musica}.png',
                    width=150
                )

                conteudo = ft.Row(
                    controls=[
                        imagem,
                        ft.Column(
                            controls=[
                                ft.Text(nome_musica, color='#D6AB5F', size=18),
                                ft.Text(f"Artistas: {texto_autores}", color='#D6AB5F', size=12)
                            ],
                            expand=True
                        ),
                        ft.ElevatedButton(text="Editar", on_click=lambda e: self.editar_musica(e)),
                        ft.ElevatedButton(text="Excluir", on_click=lambda e, id_m=id_musica: self.excluir_musica(e, id_m))
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

    def editar_musica(self, e):
        print('editar')

    def excluir_musica(self, e, id_musica):
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM factAutorMusica WHERE id_musica = ?', (id_musica,))

            cursor.execute('DELETE FROM dimMusicas WHERE id_musica = ?', (id_musica,))

            conn.commit()
            conn.close()

            imagem_path = f'imagens_musicas/{id_musica}.png'
            if os.path.exists(imagem_path):
                os.remove(imagem_path)
                print(f"Imagem {imagem_path} removida.")

            print(f"Música com ID {id_musica} excluída com sucesso.")

            self.lista_musicas.controls.clear()
            self.carregar_musicas()

        except Exception as err:
            print("Erro ao excluir música:", err)

    def sair(self, e):
        self.sair_callback()