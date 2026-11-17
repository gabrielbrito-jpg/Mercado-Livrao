# FeiraLivrão

Marketplace estilo "feira online": o comprador começa com R$ 1000 de crédito, pesquisa, filtra, compra e avalia produtos. Feito com Flask (back-end em POO com classes e DAOs), SQLite e front-end em HTML/CSS/JS consumindo as rotas via Fetch.

## Como rodar

```bash
pip install flask
python database.py   # (opcional) recria o banco do zero com os dados de exemplo
python app.py
```

Abra http://127.0.0.1:5000 no navegador.

Para testar todas as rotas sem o navegador: `python testar_api.py` (recria o banco antes).

> Os relatórios usam RIGHT JOIN e FULL JOIN, que precisam do SQLite 3.39 ou mais novo (vem no Python 3.11+).

## Estrutura

```
app.py              rotas Flask (API JSON + página inicial)
classes.py          classes do modelo (Comprador, Produto, Compra...)
daos.py             DAOs com o SQL de cada tabela + relatórios com JOIN
database.py         conexão e criação do banco
index.html          página da loja (fica na raiz do projeto)
templates/          outras páginas: compras.html, vender.html, relatorios.html
static/css/style.css  estilo
static/js/app.js      chamadas fetch para as rotas e montagem da tela
schemas/            schema.sql, seed.sql, consultas.sql e o banco
docs/               MER, modelo lógico e diagrama de classes
```

## Páginas

| Rota | Arquivo |
|---|---|
| `/` | `index.html` (loja) |
| `/minhas-compras` | `templates/compras.html` |
| `/vender` | `templates/vender.html` |
| `/relatorios` | `templates/relatorios.html` |

## Rotas da API (usadas pelo fetch)

| Método | Rota | O que faz |
|---|---|---|
| GET | `/comprador` | saldo do comprador |
| GET/POST | `/categorias` | lista / cadastra categoria |
| GET/POST | `/vendedores` | lista / cadastra vendedor |
| GET | `/produtos?busca=&categoria=&preco_min=&preco_max=&ordem=` | pesquisa e classificação |
| GET | `/produtos/<id>` | detalhe com avaliações |
| POST | `/produtos` | cadastra produto |
| POST | `/comprar` | compra (valida saldo e estoque) |
| GET | `/compras` | histórico de compras |
| POST | `/avaliacoes` | avalia um produto comprado (nota 1 a 5) |
| GET | `/relatorios/produtos-com-nota` | LEFT JOIN |
| GET | `/relatorios/categorias` | RIGHT JOIN |
| GET | `/relatorios/vendedores-produtos` | FULL JOIN |
| GET | `/relatorios/mais-vendidos` | INNER JOIN |

## Roteiro para a apresentação

1. **Loja**: mostrar a busca ("fone"), o filtro por categoria, a faixa de preço e a ordenação (menor preço, melhor avaliados).
2. **Comprar**: comprar um produto e mostrar o saldo caindo no topo e o estoque diminuindo. Tentar comprar mais que o saldo para mostrar o erro.
3. **Avaliar**: abrir o produto comprado e enviar uma avaliação. Tentar avaliar um produto não comprado para mostrar a regra.
4. **Minhas compras**: histórico (INNER JOIN entre compra e produto).
5. **Vender**: cadastrar categoria, vendedor e um produto novo, e mostrar ele aparecendo na loja.
6. **Relatórios**: explicar cada JOIN. "Pets" aparece com 0 produtos (RIGHT JOIN), "Vendedor Fantasma" sem produtos e "Caneca de Origem Misteriosa" sem vendedor (FULL JOIN).
