CREATE TABLE comprador (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nome   TEXT NOT NULL,
    saldo  REAL DEFAULT 1000
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
    preco         REAL,
    estoque       INTEGER,
    emoji         TEXT,
    FOREIGN KEY (vendedor_id)  REFERENCES vendedor(id),
    FOREIGN KEY (categoria_id) REFERENCES categoria(id)
);

CREATE TABLE compra (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    comprador_id  INTEGER,
    produto_id    INTEGER,
    quantidade    INTEGER,
    valor_total   REAL,
    data_compra   TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comprador_id) REFERENCES comprador(id),
    FOREIGN KEY (produto_id)   REFERENCES produto(id)
);

CREATE TABLE avaliacao (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id     INTEGER,
    comprador_id   INTEGER,
    nota           INTEGER,
    comentario     TEXT,
    data_avaliacao TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id)   REFERENCES produto(id),
    FOREIGN KEY (comprador_id) REFERENCES comprador(id)
);
