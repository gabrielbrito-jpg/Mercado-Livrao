# Diagrama de Classes (UML) - Mercado Livrão

Cole o código abaixo em https://mermaid.live para ver e exportar como imagem.

```mermaid
classDiagram
    class Pessoa {
        -int _id
        -str _nome
        +id() int
        +nome() str
    }
    class Comprador {
        -float _saldo
        +saldo() float
        +tem_saldo(valor) bool
        +pagar(valor)
    }
    class Vendedor {
        -str _cidade
        +cidade() str
    }
    class Categoria {
        -int _id
        -str _nome
        +id() int
        +nome() str
    }
    class Produto {
        -int _id
        -int _vendedor_id
        -int _categoria_id
        -str _titulo
        -str _descricao
        -float _preco
        -int _estoque
        -str _emoji
        +tem_estoque(quantidade) bool
        +retirar_estoque(quantidade)
    }
    class Compra {
        -int _id
        -int _comprador_id
        -int _produto_id
        -int _quantidade
        -float _valor_total
        -str _data_compra
    }
    class Avaliacao {
        -int _id
        -int _produto_id
        -int _comprador_id
        -int _nota
        -str _comentario
        -str _data_avaliacao
    }
    class DadoInvalidoError
    class EstoqueInsuficienteError
    class SaldoInsuficienteError

    class Database {
        +conectar() Connection
        +consultar(sql, parametros) list
        +executar(sql, parametros) int
        +rodar_arquivo_sql(caminho)
        +criar_banco()
    }
    class CompradorDAO {
        +buscar(id) Comprador
        +atualizar_saldo(id, novo_saldo)
    }
    class VendedorDAO {
        +buscar(id) Vendedor
        +cadastrar(vendedor)
        +atualizar(vendedor)
        +remover(id)
        +listar()
    }
    class CategoriaDAO {
        +buscar(id) Categoria
        +cadastrar(categoria)
        +listar()
    }
    class ProdutoDAO {
        +cadastrar(produto)
        +atualizar(produto)
        +remover(id)
        +buscar(id) Produto
        +detalhe(id)
        +pesquisar(busca, categoria_id, preco_min, preco_max, ordem)
        +diminuir_estoque(id, quantidade)
    }
    class CompraDAO {
        +cadastrar(compra)
        +historico(comprador_id)
        +ja_comprou(comprador_id, produto_id) bool
        +produto_foi_vendido(produto_id) bool
    }
    class AvaliacaoDAO {
        +cadastrar(avaliacao)
        +listar_por_produto(produto_id)
    }
    class RelatorioDAO {
        +produtos_com_nota()
        +categorias_com_quantidade()
        +vendedores_e_produtos()
        +mais_vendidos()
    }

    Pessoa <|-- Comprador
    Pessoa <|-- Vendedor
    DadoInvalidoError --|> ValueError
    EstoqueInsuficienteError --|> Exception
    SaldoInsuficienteError --|> Exception
    Produto ..> EstoqueInsuficienteError : lança
    Comprador ..> SaldoInsuficienteError : lança

    Vendedor "0..1" --> "0..*" Produto : vende
    Categoria "0..1" --> "0..*" Produto : classifica
    Comprador "1" --> "0..*" Compra : realiza
    Produto "1" --> "0..*" Compra : é comprado em
    Produto "1" --> "0..*" Avaliacao : recebe
    Comprador "1" --> "0..*" Avaliacao : escreve

    CompradorDAO ..> Comprador
    VendedorDAO ..> Vendedor
    CategoriaDAO ..> Categoria
    ProdutoDAO ..> Produto
    CompraDAO ..> Compra
    AvaliacaoDAO ..> Avaliacao
    CompradorDAO ..> Database
    VendedorDAO ..> Database
    CategoriaDAO ..> Database
    ProdutoDAO ..> Database
    CompraDAO ..> Database
    AvaliacaoDAO ..> Database
    RelatorioDAO ..> Database
```

## Observações

- `vendedor_id` e `categoria_id` em Produto podem ser nulos (um produto pode não ter vendedor ou categoria). Isso permite mostrar o FULL JOIN entre vendedores e produtos.
- Os atributos das classes são protegidos (`_nome`, `_saldo`...) e acessados por `@property`; os setters validam o valor e lançam `DadoInvalidoError`.
- `Comprador` e `Vendedor` herdam de `Pessoa`.
- As rotas Flask (`app.py`) usam as classes e os DAOs acima e tratam as exceções com `try/except`.
