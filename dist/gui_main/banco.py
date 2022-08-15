import sqlite3
from sqlite3 import Error
import os

#Conexao com o banco
def conexaoBanco():
    caminhoBanco = f'{os.path.dirname(__file__)}\\itens.db'
    conexao = None
    try:
        conexao = sqlite3.connect(caminhoBanco)
    except Error as ex:
        print(ex)
    return conexao

def selecionar(sql):
    conexao = conexaoBanco()
    cursor = conexao.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    conexao.close()
    return resultado

def manipular_dados(sql): #INSERT, UPDATE, DELETE
    try:
        conexao = conexaoBanco()
        cursor = conexao.cursor()
        cursor.execute(sql)
        conexao.commit()
        conexao.close()
    except Error as ex:
        print(ex)

