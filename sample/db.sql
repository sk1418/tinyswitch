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
        UNIQUE (server, port)
    );


CREATE TABLE
    config
    (
        name TEXT NOT NULL,
        value TEXT,
        UNIQUE (name)
    );

insert into config (name,value)values('tinyproxy.bin.path',null);

insert into proxy (id, name, server, port, username, password, authstring, active, description) values (1, 'noproxy', '-NoServer-', '-NoPort-', null, null, null, 0, 'without any proxy. this proxy cannot be deleted.');


