CREATE TABLE comprador (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nome   TEXT NOT NULL,
    saldo  REAL NOT NULL DEFAULT 1000 CHECK (saldo >= 0)
);

CREATE TABLE vendedor (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nome   TEXT NOT NULL,
    cidade TEXT
);

CREATE TABLE categoria (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome  TEXT NOT NULL UNIQUE
);

-- vendedor_id e categoria_id aceitam NULL de propósito:
-- permite mostrar produto sem vendedor no FULL JOIN do relatório.
CREATE TABLE produto (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    vendedor_id   INTEGER,
    categoria_id  INTEGER,
    titulo        TEXT NOT NULL,
    descricao     TEXT,
    preco         REAL NOT NULL CHECK (preco > 0),
    estoque       INTEGER NOT NULL CHECK (estoque >= 0),
    emoji         TEXT,
    FOREIGN KEY (vendedor_id)  REFERENCES vendedor(id)  ON DELETE SET NULL,
    FOREIGN KEY (categoria_id) REFERENCES categoria(id) ON DELETE SET NULL
);

CREATE TABLE compra (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    comprador_id  INTEGER NOT NULL,
    produto_id    INTEGER NOT NULL,
    quantidade    INTEGER NOT NULL CHECK (quantidade > 0),
    valor_total   REAL NOT NULL CHECK (valor_total >= 0),
    data_compra   TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comprador_id) REFERENCES comprador(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id)   REFERENCES produto(id)   ON DELETE RESTRICT
);

CREATE TABLE avaliacao (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id     INTEGER NOT NULL,
    comprador_id   INTEGER NOT NULL,
    nota           INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5),
    comentario     TEXT,
    data_avaliacao TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id)   REFERENCES produto(id)   ON DELETE CASCADE,
    FOREIGN KEY (comprador_id) REFERENCES comprador(id) ON DELETE CASCADE
);
