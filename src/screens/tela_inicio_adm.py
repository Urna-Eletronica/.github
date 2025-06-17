import flet as ft
import sqlite3 as sql
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class TelaInicioAdm(ft.Container):
    def __init__(self, votar_callback, cadastro_m_callback, id_user):
        super().__init__()

        self.id_user = id_user

        self.cadastro_m_callback = cadastro_m_callback
        self.votar_callback = votar_callback

        self.cadastro_m = ft.ElevatedButton(
            text="Cadastrar Músicas",
            on_click=self.abrir_cadastro_m
        )

        self.iniciar = ft.ElevatedButton(
            text="Iniciar Votação",
            on_click = self.iniciar_votacao
        )

        self.encerrar = ft.ElevatedButton(
            text="Encerrar Votação",
            on_click = self.encerrar_votacao
        )

        self.votar = ft.ElevatedButton(
            text="Votar",
            on_click = self.abrir_votacao
        )

        self.content = (
            ft.Column(
                controls=[self.cadastro_m,self.iniciar,self.encerrar,self.votar]
            )
        )


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

        except Exception as err:
            print("Erro ao encerrar votação:", err)
