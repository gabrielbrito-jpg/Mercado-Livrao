from daos.comum import executar_select, executar_comando


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
