class Comprador:
    def __init__(self, id, nome, saldo):
        self.id = id
        self.nome = nome
        self.saldo = saldo

    def tem_saldo(self, valor):
        return self.saldo >= valor
