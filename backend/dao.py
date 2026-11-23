from database import Database
from models import Comprador, Vendedor, Categoria, Produto

db = Database()


class CompradorDAO:

    def buscar(self, id):
        resultado = db.consultar("SELECT * FROM comprador WHERE id = ?", [id])
        if len(resultado) == 0:
            return None
        c = resultado[0]
        return Comprador(c["id"], c["nome"], c["saldo"])

    def atualizar_saldo(self, id, novo_saldo):
        db.executar("UPDATE comprador SET saldo = ? WHERE id = ?", [novo_saldo, id])


class VendedorDAO:

    def listar(self):
        return db.consultar("SELECT * FROM vendedor")

    def buscar(self, id):
        resultado = db.consultar("SELECT * FROM vendedor WHERE id = ?", [id])
        if len(resultado) == 0:
            return None
        v = resultado[0]
        return Vendedor(v["id"], v["nome"], v["cidade"])

    def cadastrar(self, vendedor):
        return db.executar("INSERT INTO vendedor (nome, cidade) VALUES (?, ?)",
                           [vendedor.nome, vendedor.cidade])

    def atualizar(self, vendedor):
        db.executar("UPDATE vendedor SET nome = ?, cidade = ? WHERE id = ?",
                    [vendedor.nome, vendedor.cidade, vendedor.id])

    def remover(self, id):
        db.executar("DELETE FROM vendedor WHERE id = ?", [id])


class CategoriaDAO:

    def listar(self):
        return db.consultar("SELECT * FROM categoria")

    def buscar(self, id):
        resultado = db.consultar("SELECT * FROM categoria WHERE id = ?", [id])
        if len(resultado) == 0:
            return None
        c = resultado[0]
        return Categoria(c["id"], c["nome"])

    def cadastrar(self, categoria):
        return db.executar("INSERT INTO categoria (nome) VALUES (?)", [categoria.nome])


class ProdutoDAO:

    # SELECT base dos produtos: traz o nome da categoria, do vendedor,
    # a nota media e quantos ja foram vendidos
    SQL_BASE = """
        SELECT produto.id, produto.titulo, produto.descricao, produto.preco,
               produto.estoque, produto.emoji,
               categoria.nome AS categoria,
               vendedor.nome AS vendedor,
               (SELECT AVG(nota) FROM avaliacao WHERE avaliacao.produto_id = produto.id) AS nota_media,
               (SELECT SUM(quantidade) FROM compra WHERE compra.produto_id = produto.id) AS vendidos
        FROM produto
        LEFT JOIN categoria ON categoria.id = produto.categoria_id
        LEFT JOIN vendedor ON vendedor.id = produto.vendedor_id
    """

    def buscar(self, id):
        resultado = db.consultar("SELECT * FROM produto WHERE id = ?", [id])
        if len(resultado) == 0:
            return None
        p = resultado[0]
        return Produto(p["id"], p["vendedor_id"], p["categoria_id"], p["titulo"],
                       p["descricao"], p["preco"], p["estoque"], p["emoji"])

    def detalhe(self, id):
        resultado = db.consultar(self.SQL_BASE + " WHERE produto.id = ?", [id])
        if len(resultado) == 0:
            return None
        return resultado[0]

    # pesquisa com filtros opcionais e ordenacao
    def pesquisar(self, busca, categoria_id, preco_min, preco_max, ordem):
        sql = self.SQL_BASE + " WHERE 1 = 1"
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

        return db.consultar(sql, parametros)

    def cadastrar(self, produto):
        return db.executar(
            "INSERT INTO produto (vendedor_id, categoria_id, titulo, descricao, preco, estoque, emoji) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            [produto.vendedor_id, produto.categoria_id, produto.titulo,
             produto.descricao, produto.preco, produto.estoque, produto.emoji])

    def atualizar(self, produto):
        db.executar(
            "UPDATE produto SET vendedor_id = ?, categoria_id = ?, titulo = ?, descricao = ?, "
            "preco = ?, estoque = ?, emoji = ? WHERE id = ?",
            [produto.vendedor_id, produto.categoria_id, produto.titulo, produto.descricao,
             produto.preco, produto.estoque, produto.emoji, produto.id])

    def remover(self, id):
        db.executar("DELETE FROM produto WHERE id = ?", [id])

    def diminuir_estoque(self, id, quantidade):
        db.executar("UPDATE produto SET estoque = estoque - ? WHERE id = ?", [quantidade, id])


class CompraDAO:

    def cadastrar(self, compra):
        return db.executar(
            "INSERT INTO compra (comprador_id, produto_id, quantidade, valor_total) VALUES (?, ?, ?, ?)",
            [compra.comprador_id, compra.produto_id, compra.quantidade, compra.valor_total])

    # INNER JOIN: so as compras que tem produto
    def historico(self, comprador_id):
        return db.consultar("""
            SELECT compra.id, produto.titulo, produto.emoji, compra.quantidade,
                   compra.valor_total, compra.data_compra
            FROM compra
            INNER JOIN produto ON produto.id = compra.produto_id
            WHERE compra.comprador_id = ?
            ORDER BY compra.id DESC
        """, [comprador_id])

    def ja_comprou(self, comprador_id, produto_id):
        resultado = db.consultar("SELECT id FROM compra WHERE comprador_id = ? AND produto_id = ?",
                                 [comprador_id, produto_id])
        return len(resultado) > 0

    def produto_foi_vendido(self, produto_id):
        resultado = db.consultar("SELECT id FROM compra WHERE produto_id = ?", [produto_id])
        return len(resultado) > 0


class AvaliacaoDAO:

    def cadastrar(self, avaliacao):
        return db.executar(
            "INSERT INTO avaliacao (produto_id, comprador_id, nota, comentario) VALUES (?, ?, ?, ?)",
            [avaliacao.produto_id, avaliacao.comprador_id, avaliacao.nota, avaliacao.comentario])

    def listar_por_produto(self, produto_id):
        return db.consultar("""
            SELECT avaliacao.id, avaliacao.nota, avaliacao.comentario,
                   avaliacao.data_avaliacao, comprador.nome AS comprador
            FROM avaliacao
            INNER JOIN comprador ON comprador.id = avaliacao.comprador_id
            WHERE avaliacao.produto_id = ?
            ORDER BY avaliacao.id DESC
        """, [produto_id])


class RelatorioDAO:

    # LEFT JOIN: todos os produtos, mesmo os que nao tem avaliacao
    def produtos_com_nota(self):
        return db.consultar("""
            SELECT produto.titulo, AVG(avaliacao.nota) AS nota_media,
                   COUNT(avaliacao.id) AS qtd_avaliacoes
            FROM produto
            LEFT JOIN avaliacao ON avaliacao.produto_id = produto.id
            GROUP BY produto.id
        """)

    # RIGHT JOIN: todas as categorias, mesmo as que nao tem produto
    def categorias_com_quantidade(self):
        return db.consultar("""
            SELECT categoria.nome AS categoria, COUNT(produto.id) AS quantidade
            FROM produto
            RIGHT JOIN categoria ON categoria.id = produto.categoria_id
            GROUP BY categoria.id
        """)

    # FULL JOIN: vendedor sem produto e produto sem vendedor aparecem
    def vendedores_e_produtos(self):
        return db.consultar("""
            SELECT vendedor.nome AS vendedor, produto.titulo AS produto
            FROM vendedor
            FULL JOIN produto ON produto.vendedor_id = vendedor.id
        """)

    # INNER JOIN: so os produtos que ja foram vendidos
    def mais_vendidos(self):
        return db.consultar("""
            SELECT produto.titulo, SUM(compra.quantidade) AS unidades_vendidas
            FROM produto
            INNER JOIN compra ON compra.produto_id = produto.id
            GROUP BY produto.id
            ORDER BY unidades_vendidas DESC
        """)
