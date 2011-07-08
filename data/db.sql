CREATE TABLE
    proxy
    (
        id INTEGER NOT NULL,
        name TEXT NOT NULL,
        server TEXT NOT NULL,
        port TEXT NOT NULL,
        username TEXT,
        password TEXT,
        authstring TEXT,
        active INTEGER NOT NULL,
        description TEXT,
        PRIMARY KEY (id),
        UNIQUE (PRIMARY),
        UNIQUE (server, port)
    );


CREATE TABLE
    config
    (
        name TEXT NOT NULL,
        value TEXT,
        UNIQUE (name)
    );
