from daos.comum import executar_select, executar_comando


class VendedorDAO:

    def cadastrar(self, vendedor):
        return executar_comando(
            "INSERT INTO vendedor (nome, cidade) VALUES (?, ?)",
            [vendedor.nome, vendedor.cidade])

    def listar(self):
        return executar_select("SELECT * FROM vendedor")
