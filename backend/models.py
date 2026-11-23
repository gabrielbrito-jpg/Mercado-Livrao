# classes que representam as tabelas do banco

class DadoInvalidoError(ValueError):
    pass


def converter(valor, tipo, mensagem):
    try:
        return tipo(valor)
    except (TypeError, ValueError):
        raise DadoInvalidoError(mensagem)


def id_opcional(valor):
    if valor is None or valor == "":
        return None
    return converter(valor, int, "Id invalido")


class Pessoa:
    def __init__(self, id, nome):
        self._id = id
        self.nome = nome

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if valor is None or str(valor).strip() == "":
            raise DadoInvalidoError("Informe o nome")
        self._nome = str(valor).strip()


class Comprador(Pessoa):
    def __init__(self, id, nome, saldo):
        super().__init__(id, nome)
        self.saldo = saldo

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        valor = converter(valor, float, "O saldo deve ser um numero")
        if valor < 0:
            raise DadoInvalidoError("O saldo nao pode ser negativo")
        self._saldo = valor

    def tem_saldo(self, valor):
        return self._saldo >= valor


class Vendedor(Pessoa):
    def __init__(self, id, nome, cidade):
        super().__init__(id, nome)
        self.cidade = cidade

    @property
    def cidade(self):
        return self._cidade

    @cidade.setter
    def cidade(self, valor):
        self._cidade = "" if valor is None else str(valor).strip()


class Categoria:
    def __init__(self, id, nome):
        self._id = id
        self.nome = nome

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if valor is None or str(valor).strip() == "":
            raise DadoInvalidoError("Informe o nome da categoria")
        self._nome = str(valor).strip()


class Produto:
    def __init__(self, id, vendedor_id, categoria_id, titulo, descricao, preco, estoque, emoji):
        self._id = id
        self.vendedor_id = vendedor_id
        self.categoria_id = categoria_id
        self.titulo = titulo
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.emoji = emoji

    @property
    def id(self):
        return self._id

    @property
    def vendedor_id(self):
        return self._vendedor_id

    @vendedor_id.setter
    def vendedor_id(self, valor):
        self._vendedor_id = id_opcional(valor)

    @property
    def categoria_id(self):
        return self._categoria_id

    @categoria_id.setter
    def categoria_id(self, valor):
        self._categoria_id = id_opcional(valor)

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        if valor is None or str(valor).strip() == "":
            raise DadoInvalidoError("Informe o titulo do produto")
        self._titulo = str(valor).strip()

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = "" if valor is None else str(valor).strip()

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, valor):
        valor = converter(valor, float, "O preco deve ser um numero")
        if valor <= 0:
            raise DadoInvalidoError("O preco deve ser maior que zero")
        self._preco = valor

    @property
    def estoque(self):
        return self._estoque

    @estoque.setter
    def estoque(self, valor):
        valor = converter(valor, int, "O estoque deve ser um numero inteiro")
        if valor < 0:
            raise DadoInvalidoError("O estoque nao pode ser negativo")
        self._estoque = valor

    @property
    def emoji(self):
        return self._emoji

    @emoji.setter
    def emoji(self, valor):
        self._emoji = valor if valor else "📦"

    def tem_estoque(self, quantidade):
        return self._estoque >= quantidade


class Compra:
    def __init__(self, id, comprador_id, produto_id, quantidade, valor_total, data_compra=None):
        self._id = id
        self._comprador_id = comprador_id
        self._produto_id = produto_id
        self.quantidade = quantidade
        self.valor_total = valor_total
        self._data_compra = data_compra

    @property
    def id(self):
        return self._id

    @property
    def comprador_id(self):
        return self._comprador_id

    @property
    def produto_id(self):
        return self._produto_id

    @property
    def quantidade(self):
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor):
        valor = converter(valor, int, "Quantidade invalida")
        if valor < 1:
            raise DadoInvalidoError("Quantidade invalida")
        self._quantidade = valor

    @property
    def valor_total(self):
        return self._valor_total

    @valor_total.setter
    def valor_total(self, valor):
        valor = converter(valor, float, "O total deve ser um numero")
        if valor < 0:
            raise DadoInvalidoError("O total nao pode ser negativo")
        self._valor_total = valor

    @property
    def data_compra(self):
        return self._data_compra


class Avaliacao:
    def __init__(self, id, produto_id, comprador_id, nota, comentario, data_avaliacao=None):
        self._id = id
        self._produto_id = produto_id
        self._comprador_id = comprador_id
        self.nota = nota
        self.comentario = comentario
        self._data_avaliacao = data_avaliacao

    @property
    def id(self):
        return self._id

    @property
    def produto_id(self):
        return self._produto_id

    @property
    def comprador_id(self):
        return self._comprador_id

    @property
    def nota(self):
        return self._nota

    @nota.setter
    def nota(self, valor):
        valor = converter(valor, int, "A nota deve ser de 1 a 5")
        if valor < 1 or valor > 5:
            raise DadoInvalidoError("A nota deve ser de 1 a 5")
        self._nota = valor

    @property
    def comentario(self):
        return self._comentario

    @comentario.setter
    def comentario(self, valor):
        self._comentario = "" if valor is None else str(valor).strip()

    @property
    def data_avaliacao(self):
        return self._data_avaliacao
