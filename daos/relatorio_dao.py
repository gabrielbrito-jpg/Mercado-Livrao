from daos.comum import executar_select


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
