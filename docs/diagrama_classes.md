# Diagrama de Classes (UML) - Mercado Livrão

Cole o código abaixo em https://mermaid.live para ver e exportar como imagem.

```mermaid
classDiagram
    class Comprador {
        +int id
        +str nome
        +float saldo
        +tem_saldo(valor) bool
    }
    class Vendedor {
        +int id
        +str nome
        +str cidade
    }
    class Categoria {
        +int id
        +str nome
    }
    class Produto {
        +int id
        +int vendedor_id
        +int categoria_id
        +str titulo
        +str descricao
        +float preco
        +int estoque
        +str emoji
        +tem_estoque(quantidade) bool
    }
    class Compra {
        +int id
        +int comprador_id
        +int produto_id
        +int quantidade
        +float valor_total
        +str data_compra
    }
    class Avaliacao {
        +int id
        +int produto_id
        +int comprador_id
        +int nota
        +str comentario
        +str data_avaliacao
    }

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
        +cadastrar(vendedor)
        +listar()
    }
    class CategoriaDAO {
        +cadastrar(categoria)
        +listar()
    }
    class ProdutoDAO {
        +cadastrar(produto)
        +buscar(id) Produto
        +detalhe(id)
        +pesquisar(busca, categoria_id, preco_min, preco_max, ordem)
        +diminuir_estoque(id, quantidade)
    }
    class CompraDAO {
        +cadastrar(compra)
        +historico(comprador_id)
        +ja_comprou(comprador_id, produto_id) bool
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
- As rotas Flask (`app.py`) usam as classes e os DAOs acima.
