from database import Database
from classes import Comprador, Vendedor, Categoria, Produto, Compra, Avaliacao

db = Database()


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


class CompradorDAO:

    def buscar(self, id):
        lista = executar_select("SELECT * FROM comprador WHERE id = ?", [id])
        if len(lista) == 0:
            return None
        c = lista[0]
        return Comprador(c["id"], c["nome"], c["saldo"])

    def atualizar_saldo(self, id, novo_saldo):
        executar_comando("UPDATE comprador SET saldo = ? WHERE id = ?", [novo_saldo, id])


class VendedorDAO:

    def cadastrar(self, vendedor):
        return executar_comando(
            "INSERT INTO vendedor (nome, cidade) VALUES (?, ?)",
            [vendedor.nome, vendedor.cidade])

    def listar(self):
        return executar_select("SELECT * FROM vendedor")


class CategoriaDAO:

    def cadastrar(self, categoria):
        return executar_comando(
            "INSERT INTO categoria (nome) VALUES (?)",
            [categoria.nome])

    def listar(self):
        return executar_select("SELECT * FROM categoria")


SQL_PRODUTOS = """
    SELECT produto.id, produto.titulo, produto.descricao, produto.preco,
           produto.estoque, produto.emoji,
           categoria.nome AS categoria, vendedor.nome AS vendedor,
           (SELECT AVG(nota) FROM avaliacao WHERE avaliacao.produto_id = produto.id) AS nota_media,
           (SELECT SUM(quantidade) FROM compra WHERE compra.produto_id = produto.id) AS vendidos
    FROM produto
    LEFT JOIN categoria ON categoria.id = produto.categoria_id
    LEFT JOIN vendedor ON vendedor.id = produto.vendedor_id
"""


class ProdutoDAO:

    def cadastrar(self, produto):
        return executar_comando(
            "INSERT INTO produto (vendedor_id, categoria_id, titulo, descricao, preco, estoque, emoji) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            [produto.vendedor_id, produto.categoria_id, produto.titulo,
             produto.descricao, produto.preco, produto.estoque, produto.emoji])

    def buscar(self, id):
        lista = executar_select("SELECT * FROM produto WHERE id = ?", [id])
        if len(lista) == 0:
            return None
        p = lista[0]
        return Produto(p["id"], p["vendedor_id"], p["categoria_id"], p["titulo"],
                       p["descricao"], p["preco"], p["estoque"], p["emoji"])

    def detalhe(self, id):
        lista = executar_select(SQL_PRODUTOS + " WHERE produto.id = ?", [id])
        if len(lista) == 0:
            return None
        return lista[0]

    def pesquisar(self, busca, categoria_id, preco_min, preco_max, ordem):
        sql = SQL_PRODUTOS + " WHERE 1 = 1"
        parametros = []

        if busca:
            sql += " AND (produto.titulo LIKE ? OR produto.descricao LIKE ?)"
            parametros.append("%" + busca + "%")
            parametros.append("%" + busca + "%")
        if categoria_id:
            sql += " AND produto.categoria_id = ?"
            parametros.append(categoria_id)
        if preco_min:
            sql += " AND produto.preco >= ?"
            parametros.append(preco_min)
        if preco_max:
            sql += " AND produto.preco <= ?"
            parametros.append(preco_max)

        if ordem == "preco_asc":
            sql += " ORDER BY produto.preco ASC"
        elif ordem == "preco_desc":
            sql += " ORDER BY produto.preco DESC"
        elif ordem == "melhor_avaliado":
            sql += " ORDER BY nota_media DESC"
        elif ordem == "mais_vendido":
            sql += " ORDER BY vendidos DESC"
        else:
            sql += " ORDER BY produto.id"

        return executar_select(sql, parametros)

    def diminuir_estoque(self, id, quantidade):
        executar_comando(
            "UPDATE produto SET estoque = estoque - ? WHERE id = ?",
            [quantidade, id])


class CompraDAO:

    def cadastrar(self, compra):
        return executar_comando(
            "INSERT INTO compra (comprador_id, produto_id, quantidade, valor_total) "
            "VALUES (?, ?, ?, ?)",
            [compra.comprador_id, compra.produto_id, compra.quantidade, compra.valor_total])

    def historico(self, comprador_id):
        return executar_select("""
            SELECT compra.id, produto.titulo, produto.emoji, compra.quantidade,
                   compra.valor_total, compra.data_compra
            FROM compra
            INNER JOIN produto ON produto.id = compra.produto_id
            WHERE compra.comprador_id = ?
            ORDER BY compra.id DESC
        """, [comprador_id])

    def ja_comprou(self, comprador_id, produto_id):
        lista = executar_select(
            "SELECT id FROM compra WHERE comprador_id = ? AND produto_id = ?",
            [comprador_id, produto_id])
        return len(lista) > 0


class AvaliacaoDAO:

    def cadastrar(self, avaliacao):
        return executar_comando(
            "INSERT INTO avaliacao (produto_id, comprador_id, nota, comentario) "
            "VALUES (?, ?, ?, ?)",
            [avaliacao.produto_id, avaliacao.comprador_id, avaliacao.nota, avaliacao.comentario])

    def listar_por_produto(self, produto_id):
        return executar_select("""
            SELECT avaliacao.id, avaliacao.nota, avaliacao.comentario,
                   avaliacao.data_avaliacao, comprador.nome AS comprador
            FROM avaliacao
            INNER JOIN comprador ON comprador.id = avaliacao.comprador_id
            WHERE avaliacao.produto_id = ?
            ORDER BY avaliacao.id DESC
        """, [produto_id])


class RelatorioDAO:

    # LEFT JOIN: todos os produtos, mesmo sem avaliação
    def produtos_com_nota(self):
        return executar_select("""
            SELECT produto.titulo, AVG(avaliacao.nota) AS nota_media,
                   COUNT(avaliacao.id) AS qtd_avaliacoes
            FROM produto
            LEFT JOIN avaliacao ON avaliacao.produto_id = produto.id
            GROUP BY produto.id
        """)

    # RIGHT JOIN: todas as categorias, mesmo sem produto
    def categorias_com_quantidade(self):
        return executar_select("""
            SELECT categoria.nome AS categoria, COUNT(produto.id) AS quantidade
            FROM produto
            RIGHT JOIN categoria ON categoria.id = produto.categoria_id
            GROUP BY categoria.id
        """)

    # FULL JOIN: vendedores sem produto e produtos sem vendedor
    def vendedores_e_produtos(self):
        return executar_select("""
            SELECT vendedor.nome AS vendedor, produto.titulo AS produto
            FROM vendedor
            FULL JOIN produto ON produto.vendedor_id = vendedor.id
        """)

    # INNER JOIN + GROUP BY: só produtos que já foram vendidos
    def mais_vendidos(self):
        return executar_select("""
            SELECT produto.titulo, SUM(compra.quantidade) AS unidades_vendidas
            FROM produto
            INNER JOIN compra ON compra.produto_id = produto.id
            GROUP BY produto.id
            ORDER BY unidades_vendidas DESC
        """)
