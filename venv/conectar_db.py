import sqlalchemy
from sqlalchemy import text
from sqlalchemy import create_engine
import mysql.connector
import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import time
from datetime import datetime
import numpy as np
from tkinter import messagebox

class conectar_db_r:
    def __init__(self,status_login,host,user,port,password,database,tabela):
        self.status_login = status_login
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database
        self.tabela = tabela
        self.lista_colunas = []
        self.lista_linhas = []


    def login(self):
        url = "mysql://{0}:{1}@{2}:{3}/{4}".format(self.user,
                                                   self.password,
                                                   self.host,
                                                   self.port,
                                                   self.database)
        try:
            sqlEngine = create_engine(url)
            self.dbConnection = sqlEngine.connect()
            self.status_login = True
            # print('Conectado')
            return self.dbConnection ,self.status_login
        except:
            self.status_login = False
            self.dbConnection = ''
            # print('Erro')
            return self.dbConnection,self.status_login


    def exec_dql(self):
        conect = self.dbConnection
        sql_table = conect.execute(text(f"select * from {self.tabela};"))
        nome_das_colunas = conect.execute(text(f"""select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS
                                                                   WHERE TABLE_NAME = '{self.tabela}'"""))
        for coluna in nome_das_colunas:
            self.lista_colunas.append(coluna[0])
        for linha in sql_table:
            self.lista_linhas.append(linha)

    def cols(self,lista_fconcat):
        valor_antes = ''
        for valor in lista_fconcat:
            if valor_antes == '':
                valor_antes = valor
            else:
                valor_antes = valor_antes + ',' + valor
        return valor_antes

    def adicionar_nf_mysql(self,chave,conexao):
        root = ET.parse(chave).getroot()  # abrir xml e 'parcing'
        http = "http://www.portalfiscal.inf.br/nfe"  # definir prefixo para pesquisa
        nsNFE = {'ns': http}  # dicionario para usar prefixo criado para 'find' no xml da NFe
        lis = ['nNF', 'cProd', 'xProd', 'uCom', 'qCom', 'vUnCom', 'vProd','indTot', 'chave_de_acesso']
        lista_de_elementos = []
        lista_de_valores = []
        tabela_nf = pd.DataFrame(columns=lis, index=range(0))

        for dados_compra in root.findall('ns:NFe/ns:infNFe/ns:det/ns:prod', nsNFE):  # mapear itens
            numero_nota_fiscal = root.find('ns:NFe/ns:infNFe/ns:ide/ns:nNF', nsNFE).text  # numero da nota fiscal
            acess_key_nf = root.find('ns:NFe')
            for element in dados_compra.iter():  # mapear elementos dos itens
                elementos_prod = element.tag.replace(http, '')
                elementos_prod = elementos_prod.replace('{}', '')  # elemento tratado
                if elementos_prod in lis:
                    valores_prod = element.text  # valor dos elementos
                    if valores_prod is None:  # Tranformando valores vazios em NA para funcionar o codigo
                        valores_prod = 'NA'
                    acess_key_nf = root.find('ns:NFe/ns:infNFe', nsNFE).attrib['Id'][3:]  # chave de acesso
                    lista_de_elementos.append(elementos_prod)
                    lista_de_valores.append(valores_prod)
            dicionario = dict(zip(tuple(lista_de_elementos), tuple(lista_de_valores)))
            dicionario.update({'nNF': numero_nota_fiscal})
            dicionario.update({'chave_de_acesso': acess_key_nf})
            tabela_nf.loc[len(tabela_nf)] = dicionario
            lista_de_elementos = []
            lista_de_valores = []
        # #tratar tabela
        tabela_nf['nNF'] = tabela_nf['nNF'].astype('int64')
        tabela_nf['qCom'] = tabela_nf['qCom'].astype('float64')
        tabela_nf['vUnCom'] = tabela_nf['vUnCom'].astype('float64')
        tabela_nf['vProd'] = tabela_nf['vProd'].astype('float64')
        tabela_nf['indTot'] = tabela_nf['indTot'].astype('int64')

        # pegar data de modificação da pasta
        ti_m = os.path.getmtime(chave)
        m_ti = time.ctime(ti_m)
        t_obj = time.strptime(m_ti)
        T_stamp = time.strftime("%Y-%m-%d", t_obj)
        data_lanc = T_stamp

        # pegar FORNECEDOR
        for dados_emit in root.findall('ns:NFe/ns:infNFe/ns:emit', nsNFE):
            for element_emit in dados_emit.iter():
                elementos_emit = element_emit.tag.replace(http, '')
                elementos_emit = elementos_emit.replace('{}', '')
                if elementos_emit == 'xNome':
                    fornecedor = element_emit.text
        for x in range(len(tabela_nf)):
            linha_tabela = tabela_nf.iloc[x].tolist()
            linha_tabela.append(data_lanc)
            linha_tabela.append(fornecedor)
            tuplas = tuple(linha_tabela)
            comando_insert = f"""INSERT INTO info_nf1 
                                ({self.cols(tabela_nf.columns)},
                                data_entrada,
                                fornecedor)
                            VALUES {tuplas};"""
            self.login().execute(text(comando_insert))
        comando_deletar_duplicado = f"""delete t1 FROM {self.tabela} t1
                                    INNER  JOIN {self.tabela} t2
                                    WHERE
                                        t1.id_sql > t2.id_sql AND
                                        t1.cProd = t2.cProd AND
                                        t1.chave_de_acesso = t2.chave_de_acesso AND
                                        t1.vProd = t2.vProd;"""
        # self.login().execute(text(comando_deletar_duplicado))

        print('deletado')