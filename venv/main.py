import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import auto
import conectar_db
import manual


tela_principal = '600x300+350+100' #variavel para tamanho da tela
class janela_empresa:
    def __init__(self):
        self.logado_com_banco_de_dados = False
        self.root = Tk()
        self.config()
        self.frames()
        self.widgets()
        self.root.mainloop()
    def config(self):
        self.root.geometry(tela_principal)
        self.root.title('Interface gráfica')
    def frames(self):
        self.frame_entrada = Frame(self.root)
        self.frame_visualizar = Frame(self.root)
        self.frame_entrada.pack()
        self.frame_visualizar.pack()
    def widgets(self):
        self.entrada_texto = Label(self.frame_entrada,
                                   text='Adicionar ao banco de dados:')
        self.entrada_manual = Button(self.frame_entrada,
                                     text='Manual',
                                     command=self.bt_entrada_manual)
        self.entrada_auto = Button(self.frame_entrada,
                                   text='Automático',
                                   command=self.bt_entrada_auto)
        self.bt_ver_tabela = Button(self.frame_visualizar,
                                    text='Ver tabela',
                                    command=self.abrir_tabela)

        self.entrada_texto.grid(row=0,column=0)
        self.entrada_manual.grid(row=0,column=1)
        self.entrada_auto.grid(row=0,column=2)
        self.bt_ver_tabela.grid(row=0,column=0)

    def esconder(self):
        self.root.withdraw() #comando para esconder janela
    def login_tabela(self):
        self.esconder() #Chama a função para esconder a janela principal

        self.janela_login_db = tkinter.Toplevel()
        self.janela_login_db.geometry('300x150+350+100')
        self.janela_login_db.title('Login Banco de dados')

        #Frames
        self.frame_label = Frame(self.janela_login_db)
        self.frame_botoes = Frame(self.janela_login_db)
        self.frame_label.pack()
        self.frame_botoes.pack()

        #Labels
        self.host_texto = Label(self.frame_label, text='Host: ')
        self.user_texto = Label(self.frame_label, text='User: ')
        self.port_texto = Label(self.frame_label, text='Port: ')
        self.password_texto = Label(self.frame_label, text='Password: ')
        self.database_texto = Label(self.frame_label, text='Database: ')
        self.tabela_texto = Label(self.frame_label, text='Tabela: ')

        #Exibir grids
        self.host_texto.grid(row=1,column=0)
        self.user_texto.grid(row=2,column=0)
        self.port_texto.grid(row=3,column=0)
        self.password_texto.grid(row=4,column=0)
        self.database_texto.grid(row=5,column=0)
        self.tabela_texto.grid(row=6, column=0)

        #Entrys (Campos de entradas)
        self.host_entry = Entry(self.frame_label)
        self.user_entry = Entry(self.frame_label)
        self.port_entry = Entry(self.frame_label)
        self.password_entry = Entry(self.frame_label)
        self.database_entry = Entry(self.frame_label)
        self.tabela_entry = Entry(self.frame_label)

        self.host_entry.insert(0, 'localhost')
        self.user_entry.insert(0, 'root')
        self.port_entry.insert(0, '3306')
        self.password_entry.insert(0, '')
        self.database_entry.insert(0, 'notas_fiscais')
        self.tabela_entry.insert(0, 'info_nf1')

        # exibir entrys
        self.host_entry.grid(row=1,column=1)
        self.user_entry.grid(row=2,column=1)
        self.port_entry.grid(row=3,column=1)
        self.password_entry.grid(row=4,column=1)
        self.database_entry.grid(row=5,column=1)
        self.tabela_entry.grid(row=6, column=1)

        self.btn_confirmar = Button(self.frame_botoes,
                                    text='Confirmar',
                                    command=self.checar_campos)

        self.botao_menu(self.frame_botoes,self.fecharframe,
                        self.janela_login_db.destroy)

        self.btn_confirmar.grid(row=0, column=1)
    def botao_menu(self,frame,func1,func2):
        self.bt_home = Button(frame,
                                text='Menu',
                                command=lambda:[func1(),func2()])
        self.bt_home.grid(row=0, column=0)

    def fecharframe(self):
        self.root.deiconify() #Chama a função inicial (Abre a janela inicial)
    def checar_campos(self):
        if (self.host_entry.get() \
            and self.user_entry.get() \
            and self.port_entry.get() \
            and self.password_entry.get() \
            and self.database_entry.get() \
            and self.tabela_entry.get()) == '':

            messagebox.showerror('Campo Vazio','Por favor complete todos os campos')
        else:
            self.entrar_db = conectar_db.conectar_db_r(self.host_entry.get(),
                                                       self.user_entry.get(),
                                                       self.port_entry.get(),
                                                       self.password_entry.get(),
                                                       self.database_entry.get(),
                                                       self.tabela_entry.get())
            # self.conect = self.entrar_db.login()
            messagebox.showinfo('Conectado','Login efetuado com sucesso')
            self.logado_com_banco_de_dados = True
            self.janela_login_db.withdraw()
            self.root.deiconify()

    def bt_entrada_auto(self):
        if self.logado_com_banco_de_dados:
            classe_auto = auto.ler_nf_auto(self.entrar_db)
            classe_auto.criar_janela()
        else:
            self.login_tabela()
    def bt_entrada_manual(self):
        if self.logado_com_banco_de_dados:
            manual.ler_nf_manual.criar_janela(self)
        else:
            self.login_tabela()
    def abrir_tabela(self):
        if self.logado_com_banco_de_dados:
            self.entrar_db.exec_dql()
            self.linha = self.entrar_db.lista_linhas
            self.coluna = self.entrar_db.lista_colunas

            self.janela_tabela = tkinter.Toplevel()
            self.janela_tabela.overrideredirect(True)
            self.janela_tabela.state('zoomed')
            self.janela_tabela.title(f'Tabela {self.tabela_entry.get()}')

            self.frame_tabela = Frame(self.janela_tabela)
            self.frame_tabela.pack()
            self.treeview_table = Treeview(self.frame_tabela,
                                           columns=(self.coluna),
                                           selectmode='browse',
                                           show='headings')
            for n_coluna in self.coluna:
                self.treeview_table.heading(n_coluna,anchor='center',text=f'{n_coluna}')
            for n_linha in self.linha:
                lista_valor = []
                for col in range(len(n_linha)):
                    self.treeview_table.column(column=col,width=110,anchor='center',stretch=True)
                for itens in n_linha:
                    lista_valor.append(itens)
                self.treeview_table.insert('','end',iid=n_linha[0],values=lista_valor)
            self.treeview_table.grid(pady=20,padx=20)
        else:
            self.login_tabela()

janela_empresa()

