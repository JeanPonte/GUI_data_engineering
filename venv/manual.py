import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import conectar_db
class ler_nf_manual:
    def criar_janela(self):
        self.janela_manual = tkinter.Toplevel()
        self.janela_manual.geometry('600x300+250+100')
        self.janela_manual.title('Entrada Manual de Dados')

