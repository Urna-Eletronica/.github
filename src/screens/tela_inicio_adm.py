import flet as ft
import sqlite3 as sql

class TelaInicioAdm(ft.Container):
    def __init__(self, votar_callback, cadastro_m_callback, id_user):
        super().__init__()

        self.id_user = id_user

        self.cadastro_m_callback = cadastro_m_callback
        # self.cadastro_g_callback = cadastro_g_callback
        self.votar_callback = votar_callback

        self.cadastro_m = ft.ElevatedButton(
            text="Cadastrar Músicas",
            on_click=self.abrir_cadastro_m
        )

        self.cadastro_g = ft.ElevatedButton(
            text="Cadastrar Gênero"
        )

        self.votar = ft.ElevatedButton(
            text="Votar",
            on_click = self.abrir_votacao
        )

        self.content = (
            ft.Column(
                controls=[self.cadastro_m,self.cadastro_g,self.votar]
            )
        )

    def abrir_votacao(self, e):
        self.votar_callback()

    def abrir_cadastro_m(self, e):
        self.cadastro_m_callback()