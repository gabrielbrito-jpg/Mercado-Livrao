-- INNER JOIN: produtos com categoria e vendedor
SELECT produto.titulo, produto.preco, categoria.nome, vendedor.nome
FROM produto
INNER JOIN categoria ON categoria.id = produto.categoria_id
INNER JOIN vendedor ON vendedor.id = produto.vendedor_id;

-- LEFT JOIN: todos os produtos com a nota média (mesmo sem avaliação)
SELECT produto.titulo, AVG(avaliacao.nota)
FROM produto
LEFT JOIN avaliacao ON avaliacao.produto_id = produto.id
GROUP BY produto.titulo;

-- RIGHT JOIN: todas as categorias com a quantidade de produtos (mesmo vazias)
SELECT categoria.nome, COUNT(produto.id)
FROM produto
RIGHT JOIN categoria ON categoria.id = produto.categoria_id
GROUP BY categoria.nome;

-- FULL JOIN: vendedores e produtos (mesmo sem ligação)
SELECT vendedor.nome, produto.titulo
FROM vendedor
FULL JOIN produto ON produto.vendedor_id = vendedor.id;

-- PESQUISA: produtos pelo nome
SELECT titulo, preco
FROM produto
WHERE titulo LIKE '%fone%';
