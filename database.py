import sqlite3
import os

ARQUIVO_BANCO = "feiralivrao.db"


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
        self.executar_arquivo("schema.sql")
        self.executar_arquivo("seed.sql")


if __name__ == "__main__":
    db = Database()
    db.criar_banco()
    print("Banco criado com sucesso!")
