from daos.database import Database

db = Database()


# funcoes usadas por todos os DAOs

def executar_select(sql, parametros=[]):
    conexao = db.conectar()
    try:
        linhas = conexao.execute(sql, parametros).fetchall()
    finally:
        conexao.close()
    lista = []
    for linha in linhas:
        lista.append(dict(linha))
    return lista


def executar_comando(sql, parametros=[]):
    conexao = db.conectar()
    try:
        cursor = conexao.execute(sql, parametros)
        conexao.commit()
        novo_id = cursor.lastrowid
    finally:
        conexao.close()
    return novo_id
