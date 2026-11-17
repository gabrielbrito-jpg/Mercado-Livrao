function dinheiro(valor) {
    return "R$ " + Number(valor).toFixed(2).replace(".", ",");
}

function texto(valor) {
    if (valor === null || valor === undefined) {
        return "-";
    }
    var div = document.createElement("div");
    div.textContent = valor;
    return div.innerHTML;
}

function mostrarMensagem(texto, tipo) {
    var caixa = document.getElementById("mensagem");
    caixa.innerHTML = '<div class="' + tipo + '">' + texto + "</div>";
    setTimeout(function () {
        caixa.innerHTML = "";
    }, 4000);
}

// faz a chamada para as rotas do Flask
async function chamar(url, metodo, dados) {
    var opcoes = { method: metodo || "GET" };
    if (dados) {
        opcoes.headers = { "Content-Type": "application/json" };
        opcoes.body = JSON.stringify(dados);
    }
    var resposta = await fetch(url, opcoes);
    var json = await resposta.json();
    return { ok: resposta.ok, dados: json };
}

// ---------- abas ----------

function mostrarAba(nome) {
    var abas = ["loja", "compras", "vender", "relatorios"];
    for (var i = 0; i < abas.length; i++) {
        document.getElementById(abas[i]).hidden = true;
        document.getElementById("aba-" + abas[i]).classList.remove("ativa");
    }
    document.getElementById(nome).hidden = false;
    document.getElementById("aba-" + nome).classList.add("ativa");

    if (nome == "compras") {
        carregarCompras();
    }
    if (nome == "relatorios") {
        carregarRelatorios();
    }
}

// ---------- saldo ----------

async function carregarSaldo() {
    var r = await chamar("/comprador");
    document.getElementById("saldo").textContent = dinheiro(r.dados.saldo);
}

// ---------- categorias e vendedores ----------

async function carregarCategorias() {
    var r = await chamar("/categorias");
    var filtro = document.getElementById("filtro-categoria");
    var form = document.getElementById("novo-categoria");

    filtro.innerHTML = '<option value="">Todas as categorias</option>';
    form.innerHTML = '<option value="">Sem categoria</option>';

    for (var i = 0; i < r.dados.length; i++) {
        var c = r.dados[i];
        filtro.innerHTML += '<option value="' + c.id + '">' + texto(c.nome) + "</option>";
        form.innerHTML += '<option value="' + c.id + '">' + texto(c.nome) + "</option>";
    }
}

async function carregarVendedores() {
    var r = await chamar("/vendedores");
    var form = document.getElementById("novo-vendedor");
    form.innerHTML = '<option value="">Sem vendedor</option>';

    for (var i = 0; i < r.dados.length; i++) {
        var v = r.dados[i];
        form.innerHTML += '<option value="' + v.id + '">' + texto(v.nome) + "</option>";
    }
}

// ---------- loja ----------

function estrelas(nota) {
    if (nota === null) {
        return "Sem avaliações";
    }
    var cheias = Math.round(nota);
    var texto = "";
    for (var i = 1; i <= 5; i++) {
        texto += i <= cheias ? "★" : "☆";
    }
    return texto + " " + Number(nota).toFixed(1);
}

async function buscarProdutos() {
    var url = "/produtos?";
    url += "busca=" + encodeURIComponent(document.getElementById("busca").value);
    url += "&categoria=" + document.getElementById("filtro-categoria").value;
    url += "&preco_min=" + document.getElementById("preco-min").value;
    url += "&preco_max=" + document.getElementById("preco-max").value;
    url += "&ordem=" + document.getElementById("ordem").value;

    var r = await chamar(url);
    var area = document.getElementById("produtos");
    area.innerHTML = "";

    if (r.dados.length == 0) {
        area.innerHTML = "<p>Nenhum produto encontrado.</p>";
        return;
    }

    for (var i = 0; i < r.dados.length; i++) {
        var p = r.dados[i];
        var estoqueTexto = p.estoque > 0 ? p.estoque + " un." : "Esgotado";
        var estoqueClasse = p.estoque > 0 ? "estoque" : "estoque acabou";

        area.innerHTML +=
            '<div class="card">' +
            '<div class="emoji" onclick="abrirDetalhe(' + p.id + ')">' + texto(p.emoji) + "</div>" +
            '<div class="corpo">' +
            '<h3 onclick="abrirDetalhe(' + p.id + ')">' + texto(p.titulo) + "</h3>" +
            '<div class="campo"><span class="rotulo">Preço</span><span class="valor preco">' + dinheiro(p.preco) + "</span></div>" +
            '<div class="colunas">' +
            '<div class="campo"><span class="rotulo">Estoque</span><span class="valor ' + estoqueClasse + '">' + estoqueTexto + "</span></div>" +
            '<div class="campo"><span class="rotulo">Avaliação</span><span class="valor nota">' + estrelas(p.nota_media) + "</span></div>" +
            "</div>" +
            '<div class="campo"><span class="rotulo">Vendedor</span><span class="valor">' + (p.vendedor ? texto(p.vendedor) : "Sem vendedor") + "</span></div>" +
            '<div class="acoes">' +
            '<input type="number" id="qtd-' + p.id + '" value="1" min="1">' +
            '<button onclick="comprar(' + p.id + ')"' + (p.estoque > 0 ? "" : " disabled") + ">" +
            (p.estoque > 0 ? "Comprar" : "Esgotado") + "</button>" +
            "</div></div></div>";
    }
}

function limparFiltros() {
    document.getElementById("busca").value = "";
    document.getElementById("filtro-categoria").value = "";
    document.getElementById("preco-min").value = "";
    document.getElementById("preco-max").value = "";
    document.getElementById("ordem").value = "";
    buscarProdutos();
}

async function comprar(id) {
    var quantidade = document.getElementById("qtd-" + id).value;
    var r = await chamar("/comprar", "POST", { produto_id: id, quantidade: quantidade });

    if (r.ok) {
        mostrarMensagem("Compra realizada! Total: " + dinheiro(r.dados.total), "ok");
        carregarSaldo();
        buscarProdutos();
    } else {
        mostrarMensagem(r.dados.erro, "erro");
    }
}

// ---------- detalhe e avaliacao ----------

async function abrirDetalhe(id) {
    var r = await chamar("/produtos/" + id);
    var p = r.dados;

    var html =
        '<div class="detalhe-emoji">' + texto(p.emoji) + "</div>" +
        '<div class="detalhe-corpo">' +
        "<h2>" + texto(p.titulo) + "</h2>" +
        '<div class="campo"><span class="rotulo">Preço</span><span class="valor preco">' + dinheiro(p.preco) + "</span></div>" +
        '<div class="colunas">' +
        '<div class="campo"><span class="rotulo">Estoque</span><span class="valor">' + p.estoque + " un.</span></div>" +
        '<div class="campo"><span class="rotulo">Avaliação</span><span class="valor nota">' + estrelas(p.nota_media) + "</span></div>" +
        "</div>" +
        '<div class="colunas">' +
        '<div class="campo"><span class="rotulo">Categoria</span><span class="valor">' + (p.categoria ? texto(p.categoria) : "Sem categoria") + "</span></div>" +
        '<div class="campo"><span class="rotulo">Vendedor</span><span class="valor">' + (p.vendedor ? texto(p.vendedor) : "Sem vendedor") + "</span></div>" +
        "</div>" +
        '<div class="campo"><span class="rotulo">Descrição</span><span class="valor">' + texto(p.descricao) + "</span></div>" +
        '<button class="botao-largo" onclick="comprarDoDetalhe(' + id + ')"' + (p.estoque > 0 ? "" : " disabled") + ">" +
        (p.estoque > 0 ? "Comprar" : "Esgotado") + "</button>" +
        "<h3>Avaliações</h3>";

    if (p.avaliacoes.length == 0) {
        html += "<p>Ninguém avaliou ainda.</p>";
    }
    for (var i = 0; i < p.avaliacoes.length; i++) {
        var a = p.avaliacoes[i];
        html += '<div class="avaliacao"><span class="rotulo">' + texto(a.comprador) + " · " + estrelas(a.nota) +
            '</span><span class="valor">' + texto(a.comentario) + "</span></div>";
    }

    html +=
        '<div class="form-avaliar">' +
        "<h3>Avaliar este produto</h3>" +
        '<select id="av-nota">' +
        '<option value="5">5 - Ótimo</option><option value="4">4 - Bom</option>' +
        '<option value="3">3 - Normal</option><option value="2">2 - Ruim</option>' +
        '<option value="1">1 - Péssimo</option></select>' +
        '<textarea id="av-comentario" placeholder="Comentário"></textarea>' +
        '<button onclick="enviarAvaliacao(' + id + ')">Enviar avaliação</button>' +
        "</div></div>";

    document.getElementById("detalhe").innerHTML = html;
    document.getElementById("modal").showModal();
}

async function comprarDoDetalhe(id) {
    var r = await chamar("/comprar", "POST", { produto_id: id, quantidade: 1 });

    if (r.ok) {
        mostrarMensagem("Compra realizada! Total: " + dinheiro(r.dados.total), "ok");
        carregarSaldo();
        buscarProdutos();
        abrirDetalhe(id);
    } else {
        mostrarMensagem(r.dados.erro, "erro");
    }
}

async function enviarAvaliacao(id) {
    var nota = document.getElementById("av-nota").value;
    var comentario = document.getElementById("av-comentario").value;
    var r = await chamar("/avaliacoes", "POST", { produto_id: id, nota: nota, comentario: comentario });

    if (r.ok) {
        mostrarMensagem("Avaliação enviada!", "ok");
        abrirDetalhe(id);
        buscarProdutos();
    } else {
        mostrarMensagem(r.dados.erro, "erro");
    }
}

function fecharModalBotao() {
    document.getElementById("modal").close();
}

// ---------- minhas compras ----------

async function carregarCompras() {
    var r = await chamar("/compras");
    var corpo = document.getElementById("lista-compras");
    corpo.innerHTML = "";

    if (r.dados.length == 0) {
        corpo.innerHTML = '<tr><td colspan="5">Você ainda não comprou nada.</td></tr>';
    }
    for (var i = 0; i < r.dados.length; i++) {
        var c = r.dados[i];
        corpo.innerHTML += "<tr><td>" + texto(c.emoji) + "</td><td>" + texto(c.titulo) + "</td><td>" +
            c.quantidade + "</td><td>" + dinheiro(c.valor_total) + "</td><td>" + texto(c.data_compra) + "</td></tr>";
    }
}

// ---------- vender (cadastros) ----------

async function cadastrarProduto() {
    var dados = {
        titulo: document.getElementById("novo-titulo").value,
        descricao: document.getElementById("novo-descricao").value,
        preco: document.getElementById("novo-preco").value,
        estoque: document.getElementById("novo-estoque").value,
        emoji: document.getElementById("novo-emoji").value || "📦",
        categoria_id: document.getElementById("novo-categoria").value || null,
        vendedor_id: document.getElementById("novo-vendedor").value || null
    };
    var r = await chamar("/produtos", "POST", dados);

    if (r.ok) {
        mostrarMensagem("Produto cadastrado!", "ok");
        document.getElementById("novo-titulo").value = "";
        document.getElementById("novo-descricao").value = "";
        document.getElementById("novo-preco").value = "";
        buscarProdutos();
    } else {
        mostrarMensagem(r.dados.erro, "erro");
    }
}

async function cadastrarVendedor() {
    var dados = {
        nome: document.getElementById("vend-nome").value,
        cidade: document.getElementById("vend-cidade").value
    };
    var r = await chamar("/vendedores", "POST", dados);

    if (r.ok) {
        mostrarMensagem("Vendedor cadastrado!", "ok");
        document.getElementById("vend-nome").value = "";
        document.getElementById("vend-cidade").value = "";
        carregarVendedores();
    } else {
        mostrarMensagem(r.dados.erro, "erro");
    }
}

async function cadastrarCategoria() {
    var r = await chamar("/categorias", "POST", { nome: document.getElementById("cat-nome").value });

    if (r.ok) {
        mostrarMensagem("Categoria cadastrada!", "ok");
        document.getElementById("cat-nome").value = "";
        carregarCategorias();
    } else {
        mostrarMensagem(r.dados.erro, "erro");
    }
}

// ---------- relatorios ----------

async function carregarRelatorios() {
    var r1 = await chamar("/relatorios/produtos-com-nota");
    var corpo = document.getElementById("rel-notas");
    corpo.innerHTML = "";
    for (var i = 0; i < r1.dados.length; i++) {
        var a = r1.dados[i];
        corpo.innerHTML += "<tr><td>" + texto(a.titulo) + "</td><td>" +
            (a.nota_media === null ? "-" : Number(a.nota_media).toFixed(1)) + "</td><td>" + a.qtd_avaliacoes + "</td></tr>";
    }

    var r2 = await chamar("/relatorios/categorias");
    corpo = document.getElementById("rel-categorias");
    corpo.innerHTML = "";
    for (i = 0; i < r2.dados.length; i++) {
        var b = r2.dados[i];
        corpo.innerHTML += "<tr><td>" + texto(b.categoria) + "</td><td>" + b.quantidade + "</td></tr>";
    }

    var r3 = await chamar("/relatorios/vendedores-produtos");
    corpo = document.getElementById("rel-vendedores");
    corpo.innerHTML = "";
    for (i = 0; i < r3.dados.length; i++) {
        var c = r3.dados[i];
        corpo.innerHTML += "<tr><td>" + (c.vendedor === null ? "(sem vendedor)" : texto(c.vendedor)) + "</td><td>" +
            (c.produto === null ? "(sem produtos)" : texto(c.produto)) + "</td></tr>";
    }

    var r4 = await chamar("/relatorios/mais-vendidos");
    corpo = document.getElementById("rel-vendidos");
    corpo.innerHTML = "";
    for (i = 0; i < r4.dados.length; i++) {
        var d = r4.dados[i];
        corpo.innerHTML += "<tr><td>" + texto(d.titulo) + "</td><td>" + d.unidades_vendidas + "</td></tr>";
    }
}

// ---------- ao abrir a pagina ----------

document.getElementById("busca").addEventListener("keypress", function (e) {
    if (e.key == "Enter") {
        buscarProdutos();
    }
});

carregarSaldo();
carregarCategorias();
carregarVendedores();
buscarProdutos();
