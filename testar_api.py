from daos.database import Database

# recria o banco do zero antes de testar
Database().criar_banco()

from app import app

cliente = app.test_client()


def mostrar(titulo, resposta):
    print("=====", titulo, "->", resposta.status_code)
    print(resposta.get_json())
    print()


mostrar("GET /comprador", cliente.get("/comprador"))
mostrar("GET /categorias", cliente.get("/categorias"))
mostrar("GET /vendedores", cliente.get("/vendedores"))

# pesquisa
mostrar("pesquisa: busca=fone", cliente.get("/produtos?busca=fone"))
mostrar("pesquisa: categoria=6 (Games)", cliente.get("/produtos?categoria=6"))
mostrar("pesquisa: preco ate 20, mais barato primeiro",
        cliente.get("/produtos?preco_max=20&ordem=preco_asc"))
mostrar("pesquisa: melhor avaliado", cliente.get("/produtos?ordem=melhor_avaliado"))
mostrar("GET /produtos/1", cliente.get("/produtos/1"))
mostrar("GET /produtos/999 (nao existe)", cliente.get("/produtos/999"))

# cadastros
mostrar("POST /categorias", cliente.post("/categorias", json={"nome": "Brinquedos"}))
mostrar("POST /categorias repetida", cliente.post("/categorias", json={"nome": "Brinquedos"}))
mostrar("POST /vendedores", cliente.post("/vendedores", json={"nome": "Vovo Maria", "cidade": "Santos"}))
mostrar("POST /produtos", cliente.post("/produtos", json={
    "vendedor_id": 6, "categoria_id": 8, "titulo": "Pipa Sem Vento",
    "descricao": "Voa sozinha, nem precisa de vento.", "preco": 15.5, "estoque": 4, "emoji": "🪁"}))
mostrar("POST /produtos sem preco", cliente.post("/produtos", json={"titulo": "Coisa"}))

# compras
mostrar("POST /comprar produto 2 (2 unidades)", cliente.post("/comprar", json={"produto_id": 2, "quantidade": 2}))
mostrar("GET /comprador (saldo menor)", cliente.get("/comprador"))
mostrar("POST /comprar produto 12 (5 unidades)", cliente.post("/comprar", json={"produto_id": 12, "quantidade": 5}))
mostrar("POST /comprar acima do saldo", cliente.post("/comprar", json={"produto_id": 7, "quantidade": 8}))
mostrar("GET /produtos/12 (estoque zerado)", cliente.get("/produtos/12"))
mostrar("POST /comprar acima do estoque", cliente.post("/comprar", json={"produto_id": 13, "quantidade": 99}))
mostrar("POST /comprar produto inexistente", cliente.post("/comprar", json={"produto_id": 999}))
mostrar("GET /compras", cliente.get("/compras"))

# avaliacoes
mostrar("POST /avaliacoes (comprou o 2)", cliente.post("/avaliacoes", json={"produto_id": 2, "nota": 1, "comentario": "Carregou 1% mesmo."}))
mostrar("POST /avaliacoes sem ter comprado", cliente.post("/avaliacoes", json={"produto_id": 8, "nota": 5}))
mostrar("POST /avaliacoes nota invalida", cliente.post("/avaliacoes", json={"produto_id": 2, "nota": 9}))
mostrar("GET /produtos/2 (com avaliacao nova)", cliente.get("/produtos/2"))

# relatorios (JOINs)
mostrar("relatorio LEFT JOIN", cliente.get("/relatorios/produtos-com-nota"))
mostrar("relatorio RIGHT JOIN", cliente.get("/relatorios/categorias"))
mostrar("relatorio FULL JOIN", cliente.get("/relatorios/vendedores-produtos"))
mostrar("relatorio INNER JOIN mais vendidos", cliente.get("/relatorios/mais-vendidos"))
