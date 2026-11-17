from daos.comum import executar_select, executar_comando
from models.produto import Produto


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
