from daos.comum import executar_select, executar_comando


class CategoriaDAO:

    def cadastrar(self, categoria):
        return executar_comando(
            "INSERT INTO categoria (nome) VALUES (?)",
            [categoria.nome])

    def listar(self):
        return executar_select("SELECT * FROM categoria")
