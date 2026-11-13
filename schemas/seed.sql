INSERT INTO comprador (id, nome, saldo) VALUES (1, 'Você', 1000.00);

INSERT INTO categoria (id, nome) VALUES
 (1, 'Eletrônicos'),
 (2, 'Casa e Cozinha'),
 (3, 'Moda'),
 (4, 'Esportes'),
 (5, 'Livros'),
 (6, 'Games'),
 (7, 'Pets');            -- fica sem produtos de propósito (RIGHT JOIN)

INSERT INTO vendedor (id, nome, cidade) VALUES
 (1, 'Seu Zé Gambiarra',   'Campinas'),
 (2, 'Dona Bia Promoções', 'Hortolândia'),
 (3, 'Tech do Tio Beto',   'Sumaré'),
 (4, 'Loja do Fiasco',     'Americana'),
 (5, 'Vendedor Fantasma',  'Desconhecida');   -- sem produtos (FULL JOIN)

INSERT INTO produto (id, vendedor_id, categoria_id, titulo, descricao, preco, estoque, emoji) VALUES
 (1,  3, 1, 'Fone de Ouvido Sem Fio (só o fio)', 'Tecnologia revolucionária: ele funciona exatamente como um fio.', 49.90, 20, '🎧'),
 (2,  3, 1, 'Carregador Que Carrega Só 1%', 'Ideal para quem ama emoção e viver no limite da bateria.', 29.90, 35, '🔌'),
 (3,  1, 2, 'Panela Antiaderente (Aderente Também)', 'Nada gruda... exceto o feijão do domingo.', 89.90, 12, '🍳'),
 (4,  2, 2, 'Colher de Pau Motivacional', 'Vem com frases de incentivo gravadas à mão.', 14.50, 50, '🥄'),
 (5,  2, 3, 'Meia Que Nunca Perde o Par', 'Venda de uma meia só, assim não tem como perder o par.', 9.99, 100, '🧦'),
 (6,  4, 3, 'Chinelo de Dedo Premium', 'Dedo não incluso.', 24.90, 40, '🩴'),
 (7,  1, 4, 'Bola de Futebol Quadrada', 'Para quem gosta de jogo estratégico e chute imprevisível.', 59.90, 8, '⚽'),
 (8,  4, 4, 'Haltere de Isopor 50kg', 'Parece pesado, só na aparência. Ótimo para mostrar na academia.', 79.90, 15, '🏋️'),
 (9,  2, 5, 'Livro: Como Não Perder Livros', 'Autoajuda infalível. Já vem com marcador de página.', 34.90, 25, '📚'),
 (10, 3, 6, 'Controle de Videogame Imaginário', 'Zero atraso, zero bateria, zero botões.', 19.90, 60, '🎮'),
 (11, 4, 6, 'Jogo de Tabuleiro Que Só Tem Um Lado', 'Ganha sempre, quem joga sozinho.', 69.90, 10, '🎲'),
 (12, 1, 1, 'Ventilador Que Só Gira Para Esquerda', 'Quem disse que vento precisa ser dos dois lados?', 129.90, 5, '🌀'),
 (13, NULL, 2, 'Caneca de Origem Misteriosa', 'Ninguém sabe de onde veio, mas é bonita.', 18.00, 3, '☕');   -- sem vendedor (FULL JOIN)

INSERT INTO avaliacao (produto_id, comprador_id, nota, comentario) VALUES
 (1, 1, 5, 'Funciona exatamente como prometido: é um fio.'),
 (3, 1, 4, 'Quase nada gruda. O quase é o problema.'),
 (4, 1, 5, 'Me motivou a lavar a louça.'),
 (5, 1, 3, 'Só veio uma meia, mas é verdade que nunca perdi o par.'),
 (7, 1, 2, 'Rola mal, mas é original.'),
 (9, 1, 5, 'Perdi o livro dois dias depois. Irônico.'),
 (10, 1, 4, 'Joguei 3 horas, sem lag.');

INSERT INTO compra (comprador_id, produto_id, quantidade, valor_total) VALUES
 (1, 1, 1, 49.90),
 (1, 4, 2, 29.00),
 (1, 9, 1, 34.90);

UPDATE comprador SET saldo = saldo - (49.90 + 29.00 + 34.90) WHERE id = 1;
UPDATE produto SET estoque = estoque - 1 WHERE id = 1;
UPDATE produto SET estoque = estoque - 2 WHERE id = 4;
UPDATE produto SET estoque = estoque - 1 WHERE id = 9;
