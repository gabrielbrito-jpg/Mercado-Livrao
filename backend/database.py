import sqlite3
import os

# pasta "schemas" fica na raiz do projeto (uma pasta acima do backend)
PASTA_SCHEMAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schemas")

ARQUIVO_BANCO = os.path.join(PASTA_SCHEMAS, "mercadolivrao.db")
ARQUIVO_SCHEMA = os.path.join(PASTA_SCHEMAS, "schema.sql")
ARQUIVO_SEED = os.path.join(PASTA_SCHEMAS, "seed.sql")


class Database:

    def conectar(self):
        conexao = sqlite3.connect(ARQUIVO_BANCO)
        conexao.row_factory = sqlite3.Row  # deixa acessar a coluna pelo nome
        conexao.execute("PRAGMA foreign_keys = ON")
        return conexao

    # usado no SELECT: devolve uma lista de dicionarios
    def consultar(self, sql, parametros=[]):
        conexao = self.conectar()
        try:
            linhas = conexao.execute(sql, parametros).fetchall()
        finally:
            conexao.close()  # fecha a conexao mesmo se der erro

        lista = []
        for linha in linhas:
            lista.append(dict(linha))
        return lista

    # usado no INSERT e no UPDATE: devolve o id do registro novo
    def executar(self, sql, parametros=[]):
        conexao = self.conectar()
        try:
            cursor = conexao.execute(sql, parametros)
            conexao.commit()
            novo_id = cursor.lastrowid
        finally:
            conexao.close()  # se der erro e nao fechar, o banco fica travado
        return novo_id

    def rodar_arquivo_sql(self, caminho):
        with open(caminho, encoding="utf-8") as arquivo:
            comandos = arquivo.read()

        conexao = self.conectar()
        conexao.executescript(comandos)
        conexao.commit()
        conexao.close()

    # apaga o banco e cria de novo com os dados de exemplo
    def criar_banco(self):
        if os.path.exists(ARQUIVO_BANCO):
            os.remove(ARQUIVO_BANCO)
        self.rodar_arquivo_sql(ARQUIVO_SCHEMA)
        self.rodar_arquivo_sql(ARQUIVO_SEED)


# para recriar o banco: python backend/database.py
if __name__ == "__main__":
    Database().criar_banco()
    print("Banco criado com sucesso!")
