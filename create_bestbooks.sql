CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    author VARCHAR NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    author_id INTEGER REFERENCES authors,
    year INTEGER NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books,
    user_id INTEGER REFERENCES users
);
