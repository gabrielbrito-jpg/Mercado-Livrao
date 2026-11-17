import sqlite3
import os

# caminhos a partir da pasta do projeto (funciona de qualquer lugar)
# este arquivo esta em backend/daos, entao sobe tres niveis ate a raiz
PASTA = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARQUIVO_BANCO = os.path.join(PASTA, "schemas", "feiralivrao.db")
ARQUIVO_SCHEMA = os.path.join(PASTA, "schemas", "schema.sql")
ARQUIVO_SEED = os.path.join(PASTA, "schemas", "seed.sql")


class Database:

    def conectar(self):
        conexao = sqlite3.connect(ARQUIVO_BANCO)
        conexao.row_factory = sqlite3.Row
        return conexao

    def executar_arquivo(self, nome_arquivo):
        arquivo = open(nome_arquivo, encoding="utf-8")
        comandos = arquivo.read()
        arquivo.close()

        conexao = self.conectar()
        conexao.executescript(comandos)
        conexao.commit()
        conexao.close()

    def criar_banco(self):
        if os.path.exists(ARQUIVO_BANCO):
            os.remove(ARQUIVO_BANCO)
        self.executar_arquivo(ARQUIVO_SCHEMA)
        self.executar_arquivo(ARQUIVO_SEED)

