import os
from flask import Flask, jsonify, request, render_template, send_from_directory

from database import Database, ARQUIVO_BANCO
from models import (Vendedor, Categoria, Produto, Compra, Avaliacao,
                    DadoInvalidoError, EstoqueInsuficienteError, SaldoInsuficienteError)
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

    try:
        categoria = Categoria(None, dados.get("nome"))
    except DadoInvalidoError as erro:
        return jsonify({"erro": str(erro)}), 400

    try:
        novo_id = categoria_dao.cadastrar(categoria)
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

    try:
        vendedor = Vendedor(None, dados.get("nome"), dados.get("cidade"))
    except DadoInvalidoError as erro:
        return jsonify({"erro": str(erro)}), 400

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

    try:
        produto = Produto(
            None,
            dados.get("vendedor_id"),
            dados.get("categoria_id"),
            dados.get("titulo"),
            dados.get("descricao"),
            dados.get("preco"),
            dados.get("estoque", 1),
            dados.get("emoji"))
    except DadoInvalidoError as erro:
        return jsonify({"erro": str(erro)}), 400

    novo_id = produto_dao.cadastrar(produto)
    return jsonify({"mensagem": "Produto cadastrado", "id": novo_id}), 201


@app.route("/comprar", methods=["POST"])
def comprar():
    dados = request.get_json()
    produto_id = dados.get("produto_id")

    produto = produto_dao.buscar(produto_id)
    if produto is None:
        return jsonify({"erro": "Produto nao encontrado"}), 404

    comprador = comprador_dao.buscar(COMPRADOR_ID)

    try:
        quantidade = int(dados.get("quantidade", 1))
        total = round(produto.preco * quantidade, 2)
        compra = Compra(None, COMPRADOR_ID, produto_id, quantidade, total)
        produto.retirar_estoque(quantidade)
        comprador.pagar(total)
    except (TypeError, ValueError):
        return jsonify({"erro": "Quantidade invalida"}), 400
    except EstoqueInsuficienteError as erro:
        return jsonify({"erro": str(erro)}), 400
    except SaldoInsuficienteError as erro:
        return jsonify({"erro": str(erro)}), 400

    # salva a compra, desconta o saldo e tira do estoque
    compra_dao.cadastrar(compra)
    comprador_dao.atualizar_saldo(COMPRADOR_ID, comprador.saldo)
    produto_dao.diminuir_estoque(produto_id, quantidade)

    return jsonify({"mensagem": "Compra realizada", "total": total, "saldo": comprador.saldo}), 201


@app.route("/compras")
def listar_compras():
    return jsonify(compra_dao.historico(COMPRADOR_ID))


@app.route("/avaliacoes", methods=["POST"])
def avaliar():
    dados = request.get_json()
    produto_id = dados.get("produto_id")

    try:
        avaliacao = Avaliacao(None, produto_id, COMPRADOR_ID, dados.get("nota"), dados.get("comentario"))
    except DadoInvalidoError as erro:
        return jsonify({"erro": str(erro)}), 400

    if produto_dao.buscar(produto_id) is None:
        return jsonify({"erro": "Produto nao encontrado"}), 404

    if not compra_dao.ja_comprou(COMPRADOR_ID, produto_id):
        return jsonify({"erro": "Voce so pode avaliar o que comprou"}), 400

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
