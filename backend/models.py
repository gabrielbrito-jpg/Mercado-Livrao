# classes que representam as tabelas do banco

class Comprador:
    def __init__(self, id, nome, saldo):
        self.id = id
        self.nome = nome
        self.saldo = saldo

    def tem_saldo(self, valor):
        return self.saldo >= valor


class Vendedor:
    def __init__(self, id, nome, cidade):
        self.id = id
        self.nome = nome
        self.cidade = cidade


class Categoria:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome


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


class Compra:
    def __init__(self, id, comprador_id, produto_id, quantidade, valor_total, data_compra=None):
        self.id = id
        self.comprador_id = comprador_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.valor_total = valor_total
        self.data_compra = data_compra


class Avaliacao:
    def __init__(self, id, produto_id, comprador_id, nota, comentario, data_avaliacao=None):
        self.id = id
        self.produto_id = produto_id
        self.comprador_id = comprador_id
        self.nota = nota
        self.comentario = comentario
        self.data_avaliacao = data_avaliacao
