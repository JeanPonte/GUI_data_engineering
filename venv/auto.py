import tkinter
from tkinter import *
from tkinter.ttk import *
import conectar_db
from tkinter import filedialog
import os

class ler_nf_auto:
    def __init__(self,conexao):
        self.conexao = conexao
    def abrir_dialog(self):
        mtd = conectar_db.conectar_db_r.adicionar_nf_mysql
        path = filedialog.askdirectory()
        for chave in os.listdir(path):
            mtd(self.conexao,chave=f'{path}/{chave}',conexao=self.conexao)
    def criar_janela(self):
        #Criar Janela
        self.janela_auto = tkinter.Toplevel()
        self.janela_auto.geometry('600x300+250+100')
        self.janela_auto.title('Entrada Automatica de Dados')
        # self.janela_auto.configure(bg='skyblue')

        #Frames
        self.frame_selecionar = Frame(self.janela_auto,relief=GROOVE)
        self.frame_info = Frame(self.janela_auto,relief=GROOVE)
        self.frame_visualizar = Frame(self.janela_auto,relief=GROOVE)

        self.frame_selecionar.grid(row=0,column=0,padx=20,pady=20,)
        self.frame_info.grid(row=1,column=0,padx=20,pady=20)
        self.frame_visualizar.grid(row=0,column=1,padx=20,pady=20)

        self.selecionar_pasta_text = Label(self.frame_selecionar,
                                          text='Selecione\numa pasta:')
        self.botao_navegar_pasta = Button(self.frame_selecionar,
                                        text='Navegar...',
                                        command=self.abrir_dialog)

        self.selecionar_pasta_text.grid(row=0,column=0)
        self.botao_navegar_pasta.grid(row=0,column=1)


        self.info_arq_text = Label(self.frame_info,
                                   text='Info')
        self.qnt_arq_text  = Label(self.frame_info,
                                   text='Numero de arquivos:')
        self.tipo_arq_text = Label(self.frame_info,
                                   text='Tipos de arquivos:')

        self.info_arq_text.grid(row=1, column=1)
        self.qnt_arq_text.grid( row=2, column=0,padx=10)
        self.tipo_arq_text.grid(row=3, column=0,padx=10)
