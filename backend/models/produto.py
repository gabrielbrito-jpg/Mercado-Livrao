class Produto:
    def __init__(self, id, vendedor_id, categoria_id, titulo, descricao, preco, estoque, emoji):
        self.id = id
        self.vendedor_id = vendedor_id
        self.categoria_id = categoria_id
        self.titulo = titulo
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.emoji = emoji

    def tem_estoque(self, quantidade):
        return self.estoque >= quantidade
