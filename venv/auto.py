import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import conectar_db
from tkinter import filedialog
import os
from pathlib import Path
import main

tela_principal = '200x300+150+200' #variavel para tamanho da tela
class ler_nf_auto:
    def __init__(self,dic_credencias):
        self.criar_janela()
        self.credenciais = dic_credencias

    def abrir_dialog(self):
        self.path = filedialog.askdirectory()
        qtd_file_xml = 0
        qtd_file_other = 0
        for file in os.listdir(self.path):
            file_suffix = (Path(file).suffix)  # Get Suffix
            if file_suffix == '.xml':
                qtd_file_xml += 1
            else:
                qtd_file_other +=1
        self.qnt_xml.set(qtd_file_xml)
        self.qnt_other.set(qtd_file_other)

    def ler_arquivos(self):
        entrar_db = conectar_db.conectar_db_r(True,self.credenciais['host'],
                                                   self.credenciais['user'],
                                                   self.credenciais['port'],
                                                   self.credenciais['password'],
                                                   self.credenciais['database'],
                                                   self.credenciais['tabela'])
        entrar_db.login()
        for file in os.listdir(self.path):
            file_suffix = (Path(file).suffix)  # Get Suffix
            if file_suffix == '.xml':
                entrar_db.adicionar_nf_mysql(f'{self.path}/{file}')
        messagebox.showinfo('Concluído','Arquivo(s) adicionado(s) ao banco de dados')

    def criar_janela(self):
        #Criar Janela
        self.janela_auto = tkinter.Toplevel()
        self.janela_auto.geometry(tela_principal)
        self.janela_auto.title('Entrada Automatica de Dados')
        # self.janela_auto.configure(bg='skyblue')


        #Frames
        self.frame_selecionar = Frame(self.janela_auto,relief=GROOVE)
        self.frame_info = Frame(self.janela_auto,relief=GROOVE)
        # self.frame_visualizar = Frame(self.janela_auto,relief=GROOVE)
        self.frame_home = Frame(self.janela_auto,relief=GROOVE)

        self.frame_selecionar.grid(row=0,column=0,padx=20,pady=20,)
        self.frame_info.grid(row=1,column=0,padx=20,pady=20)
        # self.frame_visualizar.grid(row=0,column=1,padx=20,pady=20)
        self.frame_home.grid(row=2,column=0)

        self.selecionar_pasta_text = Label(self.frame_selecionar,
                                          text='Selecione\numa pasta:')
        self.botao_navegar_pasta = Button(self.frame_selecionar,
                                        text='Navegar...',
                                        command=self.abrir_dialog)
        self.botao_menu = Button(self.frame_home,
                                 text='Home',
                                 command=self.janela_auto.withdraw)
        self.botao_ler_arquivos = Button(self.frame_home,
                                         text='Ler',
                                         command=self.ler_arquivos)

        self.selecionar_pasta_text.grid(row=0,column=0)
        self.botao_navegar_pasta.grid(row=0,column=1)
        self.botao_menu.grid(row=0,column=0)
        self.botao_ler_arquivos.grid(row=0,column=1)

        self.info_arq_text = Label(self.frame_info,
                                   text='Info')
        self.tipo_arq_text = Label(self.frame_info,
                                   text='Arquivos xml')
        self.qnt_arq_text  = Label(self.frame_info,
                                   text='Numero de arquivos:')
        self.qnt_other_text  = Label(self.frame_info,
                                   text='Outros arquivos:')

        self.qnt_xml = StringVar()
        self.qnt_other = StringVar()

        self.qnt_arq_var = Label(self.frame_info,textvariable=self.qnt_xml)
        self.qnt_other_var = Label(self.frame_info, textvariable=self.qnt_other)

        self.info_arq_text.grid(row=1, column=1)
        self.tipo_arq_text.grid(row=2, column=0,padx=10)
        self.qnt_arq_text.grid(row=3, column=0,padx=10)
        self.qnt_arq_var.grid(row=3, column=1)
        self.qnt_other_text.grid(row=4, column=0, padx=10)
        self.qnt_other_var.grid(row=4, column=1)