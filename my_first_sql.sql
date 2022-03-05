CREATE TABLE IF NOT EXISTS mainmenu
(
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts
(
    id integer PRIMARY KEY AUTOINCREMENT ,
    name text NOT NULL ,
    file BLOB not null ,
    wiki text NOT NULL ,
    url text NOT NULL ,
    bio text NOT NULL ,
    col1 text NOT NULL ,
    col2 text NOT NULL ,
    col3 text NOT NULL ,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS users
(
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    email text NOT NULL,
    psw text NOT NULL,
    avatar BLOB DEFAULT NULL,
    time integer NOT NULL
);