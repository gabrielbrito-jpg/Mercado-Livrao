from daos.comum import executar_select, executar_comando
from models.comprador import Comprador


class CompradorDAO:

    def buscar(self, id):
        lista = executar_select("SELECT * FROM comprador WHERE id = ?", [id])
        if len(lista) == 0:
            return None
        c = lista[0]
        return Comprador(c["id"], c["nome"], c["saldo"])

    def atualizar_saldo(self, id, novo_saldo):
        executar_comando("UPDATE comprador SET saldo = ? WHERE id = ?", [novo_saldo, id])
