import os
from flask import Flask, jsonify, request, render_template

from database import Database, ARQUIVO_BANCO
from classes import Vendedor, Categoria, Produto, Compra, Avaliacao
from daos import (CompradorDAO, VendedorDAO, CategoriaDAO, ProdutoDAO,
                  CompraDAO, AvaliacaoDAO, RelatorioDAO)

app = Flask(__name__)

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

COMPRADOR_ID = 1  # sem login, so existe um comprador


@app.route("/")
def inicio():
    return render_template("index.html")


# ---------- comprador ----------

@app.route("/comprador", methods=["GET"])
def ver_comprador():
    comprador = comprador_dao.buscar(COMPRADOR_ID)
    return jsonify({"id": comprador.id, "nome": comprador.nome, "saldo": comprador.saldo})


# ---------- categorias ----------

@app.route("/categorias", methods=["GET"])
def listar_categorias():
    return jsonify(categoria_dao.listar())


@app.route("/categorias", methods=["POST"])
def cadastrar_categoria():
    dados = request.get_json()
    if not dados or not dados.get("nome"):
        return jsonify({"erro": "Informe o nome da categoria"}), 400

    categoria = Categoria(None, dados["nome"])
    try:
        novo_id = categoria_dao.cadastrar(categoria)
    except Exception:
        return jsonify({"erro": "Essa categoria ja existe"}), 400
    return jsonify({"mensagem": "Categoria cadastrada", "id": novo_id}), 201


# ---------- vendedores ----------

@app.route("/vendedores", methods=["GET"])
def listar_vendedores():
    return jsonify(vendedor_dao.listar())


@app.route("/vendedores", methods=["POST"])
def cadastrar_vendedor():
    dados = request.get_json()
    if not dados or not dados.get("nome"):
        return jsonify({"erro": "Informe o nome do vendedor"}), 400

    vendedor = Vendedor(None, dados["nome"], dados.get("cidade", ""))
    novo_id = vendedor_dao.cadastrar(vendedor)
    return jsonify({"mensagem": "Vendedor cadastrado", "id": novo_id}), 201


# ---------- produtos ----------

# exemplo: /produtos?busca=fone&categoria=1&preco_min=10&preco_max=100&ordem=preco_asc
@app.route("/produtos", methods=["GET"])
def pesquisar_produtos():
    busca = request.args.get("busca")
    categoria = request.args.get("categoria")
    preco_min = request.args.get("preco_min")
    preco_max = request.args.get("preco_max")
    ordem = request.args.get("ordem")

    lista = produto_dao.pesquisar(busca, categoria, preco_min, preco_max, ordem)
    return jsonify(lista)


@app.route("/produtos/<int:id>", methods=["GET"])
def ver_produto(id):
    produto = produto_dao.detalhe(id)
    if produto is None:
        return jsonify({"erro": "Produto nao encontrado"}), 404

    produto["avaliacoes"] = avaliacao_dao.listar_por_produto(id)
    return jsonify(produto)


@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json()
    if not dados or not dados.get("titulo") or dados.get("preco") is None:
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


# ---------- compras ----------

@app.route("/comprar", methods=["POST"])
def comprar():
    dados = request.get_json()
    if not dados or not dados.get("produto_id"):
        return jsonify({"erro": "Informe o produto_id"}), 400

    produto_id = dados["produto_id"]
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

    compra = Compra(None, COMPRADOR_ID, produto_id, quantidade, total, None)
    compra_dao.cadastrar(compra)

    novo_saldo = round(comprador.saldo - total, 2)
    comprador_dao.atualizar_saldo(COMPRADOR_ID, novo_saldo)
    produto_dao.diminuir_estoque(produto_id, quantidade)

    return jsonify({"mensagem": "Compra realizada", "total": total, "saldo": novo_saldo}), 201


@app.route("/compras", methods=["GET"])
def listar_compras():
    return jsonify(compra_dao.historico(COMPRADOR_ID))


# ---------- avaliacoes ----------

@app.route("/avaliacoes", methods=["POST"])
def avaliar():
    dados = request.get_json()
    if not dados or not dados.get("produto_id") or not dados.get("nota"):
        return jsonify({"erro": "Informe produto_id e nota"}), 400

    produto_id = dados["produto_id"]
    nota = int(dados["nota"])

    if nota < 1 or nota > 5:
        return jsonify({"erro": "A nota deve ser de 1 a 5"}), 400

    if produto_dao.buscar(produto_id) is None:
        return jsonify({"erro": "Produto nao encontrado"}), 404

    if not compra_dao.ja_comprou(COMPRADOR_ID, produto_id):
        return jsonify({"erro": "Voce so pode avaliar o que comprou"}), 400

    avaliacao = Avaliacao(None, produto_id, COMPRADOR_ID, nota, dados.get("comentario", ""), None)
    novo_id = avaliacao_dao.cadastrar(avaliacao)
    return jsonify({"mensagem": "Avaliacao cadastrada", "id": novo_id}), 201


# ---------- relatorios (JOINs) ----------

@app.route("/relatorios/produtos-com-nota", methods=["GET"])
def relatorio_produtos_com_nota():
    return jsonify(relatorio_dao.produtos_com_nota())


@app.route("/relatorios/categorias", methods=["GET"])
def relatorio_categorias():
    return jsonify(relatorio_dao.categorias_com_quantidade())


@app.route("/relatorios/vendedores-produtos", methods=["GET"])
def relatorio_vendedores_produtos():
    return jsonify(relatorio_dao.vendedores_e_produtos())


@app.route("/relatorios/mais-vendidos", methods=["GET"])
def relatorio_mais_vendidos():
    return jsonify(relatorio_dao.mais_vendidos())


if __name__ == "__main__":
    app.run(debug=True)
