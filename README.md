# Mercado Livrão

Marketplace simples feito para o Projeto Integrado (DWS + POO + BD) do 4º bimestre, Colégio UNASP-HT, turma 2º TI-C.

O site não tem login. Existe um único comprador, que começa com R$ 1000,00 de saldo e usa esse crédito para comprar produtos de vários vendedores. Dá para pesquisar, filtrar, comprar, avaliar o que comprou, cadastrar, editar e remover produtos e vendedores, e ver relatórios feitos com INNER, LEFT, RIGHT e FULL JOIN.

## Tecnologias

- Python 3 com Flask (back-end, em POO com models, DAOs e rotas)
- SQLite (banco de dados)
- HTML, CSS e JavaScript puro, usando fetch para chamar as rotas

## Como rodar

1. Ter o Python 3 instalado. O SQLite precisa ser 3.39 ou mais novo, por causa do RIGHT JOIN e do FULL JOIN. Para conferir:

```
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

2. Instalar o Flask:

```
pip install -r requirements.txt
```

3. Criar o banco com os dados de exemplo:

```
python backend/database.py
```

4. Iniciar o servidor:

```
python backend/app.py
```

5. Abrir http://127.0.0.1:5000 no navegador.

Se o arquivo `schemas/mercadolivrao.db` não existir, o `app.py` cria o banco sozinho ao iniciar. Para voltar aos dados de exemplo, rode o passo 3 de novo.

## Estrutura de pastas

```
Mercado-Livrao/
├── backend/
│   ├── app.py          rotas do Flask
│   ├── dao.py          acesso ao banco (um DAO por entidade)
│   ├── database.py     conexão com o SQLite e criação do banco
│   └── models.py       classes, exceções e regras de negócio
├── schemas/
│   ├── schema.sql      criação das tabelas
│   ├── seed.sql        dados de exemplo
│   ├── consultas.sql   consultas com os tipos de JOIN
│   └── mercadolivrao.db
├── docs/               MER, modelo lógico e diagrama de classes
├── templates/          páginas compras, vender e relatórios
├── static/             css, js e imagens
└── index.html          página da loja
```

## Banco de dados

Seis tabelas: comprador, vendedor, categoria, produto, compra e avaliacao, ligadas por chave estrangeira. O schema usa NOT NULL e CHECK (preço maior que zero, estoque e saldo não negativos, nota de 1 a 5) e define o ON DELETE de cada chave estrangeira:

- Remover um vendedor ou uma categoria deixa os produtos dele sem vendedor ou sem categoria (SET NULL).
- Remover um produto apaga as avaliações dele (CASCADE).
- Um produto que já foi comprado não pode ser removido (RESTRICT).

## Back-end

- `models.py`: atributos protegidos com `@property` e validação nos setters. `Comprador` e `Vendedor` herdam de `Pessoa`. As exceções `DadoInvalidoError`, `EstoqueInsuficienteError` e `SaldoInsuficienteError` são tratadas com try/except nas rotas.
- `dao.py`: um DAO para cada entidade, mais o `RelatorioDAO` com os JOINs.
- `app.py`: rotas que devolvem JSON.

### Rotas principais

| Método | Rota | O que faz |
| --- | --- | --- |
| GET | /produtos | pesquisa com busca, categoria, faixa de preço e ordenação |
| GET | /produtos/id | detalhe do produto com as avaliações |
| POST | /produtos | cadastra produto |
| PUT | /produtos/id | edita produto |
| DELETE | /produtos/id | remove produto |
| GET, POST | /vendedores | lista e cadastra vendedores |
| PUT, DELETE | /vendedores/id | edita e remove vendedor |
| GET, POST | /categorias | lista e cadastra categorias |
| POST | /comprar | compra um produto |
| GET | /compras | histórico de compras |
| POST | /avaliacoes | avalia um produto comprado |
| GET | /relatorios/... | relatórios com JOIN |

## Documentação

Na pasta `docs/` estão o MER, o modelo lógico e o diagrama de classes (em Mermaid).
