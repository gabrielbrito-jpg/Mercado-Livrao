from daos.comum import executar_select, executar_comando


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
