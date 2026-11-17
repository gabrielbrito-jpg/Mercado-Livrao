import os
from flask import Flask, jsonify, request, render_template, send_from_directory

from database import Database, ARQUIVO_BANCO
from models import Vendedor, Categoria, Produto, Compra, Avaliacao
from dao import CompradorDAO, VendedorDAO, CategoriaDAO, ProdutoDAO, CompraDAO, AvaliacaoDAO, RelatorioDAO

# o front (index.html, templates e static) fica na raiz do projeto, uma pasta acima
app = Flask(__name__, template_folder="../templates", static_folder="../static")

# se o banco ainda nao existe, cria com os dados de exemplo
if not os.path.exists(ARQUIVO_BANCO):
    Database().criar_banco()

comprador_dao = CompradorDAO()
vendedor_dao = VendedorDAO()
categoria_dao = CategoriaDAO()
produto_dao = ProdutoDAO()
compra_dao = CompraDAO()
avaliacao_dao = AvaliacaoDAO()
relatorio_dao = RelatorioDAO()

COMPRADOR_ID = 1  # o site nao tem login, entao so existe um comprador


# ========== PAGINAS ==========

@app.route("/")
def pagina_loja():
    return send_from_directory("..", "index.html")


@app.route("/minhas-compras")
def pagina_compras():
    return render_template("compras.html")


@app.route("/vender")
def pagina_vender():
    return render_template("vender.html")


@app.route("/relatorios")
def pagina_relatorios():
    return render_template("relatorios.html")


# ========== API (o JavaScript chama essas rotas com fetch) ==========

@app.route("/comprador")
def ver_comprador():
    comprador = comprador_dao.buscar(COMPRADOR_ID)
    return jsonify({"id": comprador.id, "nome": comprador.nome, "saldo": comprador.saldo})


@app.route("/categorias")
def listar_categorias():
    return jsonify(categoria_dao.listar())


@app.route("/categorias", methods=["POST"])
def cadastrar_categoria():
    dados = request.get_json()
    if not dados.get("nome"):
        return jsonify({"erro": "Informe o nome da categoria"}), 400

    try:
        novo_id = categoria_dao.cadastrar(Categoria(None, dados["nome"]))
    except Exception:
        # o nome da categoria e UNIQUE no banco
        return jsonify({"erro": "Essa categoria ja existe"}), 400

    return jsonify({"mensagem": "Categoria cadastrada", "id": novo_id}), 201


@app.route("/vendedores")
def listar_vendedores():
    return jsonify(vendedor_dao.listar())


@app.route("/vendedores", methods=["POST"])
def cadastrar_vendedor():
    dados = request.get_json()
    if not dados.get("nome"):
        return jsonify({"erro": "Informe o nome do vendedor"}), 400

    vendedor = Vendedor(None, dados["nome"], dados.get("cidade", ""))
    novo_id = vendedor_dao.cadastrar(vendedor)
    return jsonify({"mensagem": "Vendedor cadastrado", "id": novo_id}), 201


# exemplo: /produtos?busca=fone&categoria=1&preco_min=10&preco_max=100&ordem=preco_asc
@app.route("/produtos")
def pesquisar_produtos():
    produtos = produto_dao.pesquisar(
        request.args.get("busca"),
        request.args.get("categoria"),
        request.args.get("preco_min"),
        request.args.get("preco_max"),
        request.args.get("ordem"))
    return jsonify(produtos)


@app.route("/produtos/<int:id>")
def ver_produto(id):
    produto = produto_dao.detalhe(id)
    if produto is None:
        return jsonify({"erro": "Produto nao encontrado"}), 404

    produto["avaliacoes"] = avaliacao_dao.listar_por_produto(id)
    return jsonify(produto)


@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json()
    if not dados.get("titulo") or not dados.get("preco"):
        return jsonify({"erro": "Informe titulo e preco"}), 400

    produto = Produto(
        None,
        dados.get("vendedor_id"),
        dados.get("categoria_id"),
        dados["titulo"],
        dados.get("descricao", ""),
        float(dados["preco"]),
        int(dados.get("estoque", 1)),
        dados.get("emoji", "📦"))

    novo_id = produto_dao.cadastrar(produto)
    return jsonify({"mensagem": "Produto cadastrado", "id": novo_id}), 201


@app.route("/comprar", methods=["POST"])
def comprar():
    dados = request.get_json()
    produto_id = dados.get("produto_id")
    quantidade = int(dados.get("quantidade", 1))

    if quantidade < 1:
        return jsonify({"erro": "Quantidade invalida"}), 400

    produto = produto_dao.buscar(produto_id)
    if produto is None:
        return jsonify({"erro": "Produto nao encontrado"}), 404

    if not produto.tem_estoque(quantidade):
        return jsonify({"erro": "Estoque insuficiente"}), 400

    comprador = comprador_dao.buscar(COMPRADOR_ID)
    total = round(produto.preco * quantidade, 2)
    if not comprador.tem_saldo(total):
        return jsonify({"erro": "Saldo insuficiente"}), 400

    # salva a compra, desconta o saldo e tira do estoque
    compra_dao.cadastrar(Compra(None, COMPRADOR_ID, produto_id, quantidade, total))
    novo_saldo = round(comprador.saldo - total, 2)
    comprador_dao.atualizar_saldo(COMPRADOR_ID, novo_saldo)
    produto_dao.diminuir_estoque(produto_id, quantidade)

    return jsonify({"mensagem": "Compra realizada", "total": total, "saldo": novo_saldo}), 201


@app.route("/compras")
def listar_compras():
    return jsonify(compra_dao.historico(COMPRADOR_ID))


@app.route("/avaliacoes", methods=["POST"])
def avaliar():
    dados = request.get_json()
    produto_id = dados.get("produto_id")
    nota = int(dados.get("nota", 0))

    if nota < 1 or nota > 5:
        return jsonify({"erro": "A nota deve ser de 1 a 5"}), 400

    if produto_dao.buscar(produto_id) is None:
        return jsonify({"erro": "Produto nao encontrado"}), 404

    if not compra_dao.ja_comprou(COMPRADOR_ID, produto_id):
        return jsonify({"erro": "Voce so pode avaliar o que comprou"}), 400

    avaliacao = Avaliacao(None, produto_id, COMPRADOR_ID, nota, dados.get("comentario", ""))
    novo_id = avaliacao_dao.cadastrar(avaliacao)
    return jsonify({"mensagem": "Avaliacao cadastrada", "id": novo_id}), 201


# ========== RELATORIOS (cada um usa um tipo de JOIN) ==========

@app.route("/relatorios/produtos-com-nota")
def relatorio_produtos_com_nota():
    return jsonify(relatorio_dao.produtos_com_nota())


@app.route("/relatorios/categorias")
def relatorio_categorias():
    return jsonify(relatorio_dao.categorias_com_quantidade())


@app.route("/relatorios/vendedores-produtos")
def relatorio_vendedores_produtos():
    return jsonify(relatorio_dao.vendedores_e_produtos())


@app.route("/relatorios/mais-vendidos")
def relatorio_mais_vendidos():
    return jsonify(relatorio_dao.mais_vendidos())


if __name__ == "__main__":
    app.run(debug=True)
