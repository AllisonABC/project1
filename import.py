import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# To set DATABASE_URL, in terminal, type: export DATABASE_URL="postgres://..."
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    f = open("books.csv")

    db.execute("CREATE TABLE authors (id SERIAL PRIMARY KEY, \
            author VARCHAR NOT NULL)")
    db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY, \
            isbn VARCHAR NOT NULL, \
            title VARCHAR NOT NULL, \
            author_id INTEGER REFERENCES authors, \
            year INTEGER NOT NULL)")
    db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, \
            username VARCHAR NOT NULL, \
            password VARCHAR(60) NOT NULL)")
    db.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, \
            rating INTEGER NOT NULL, \
            review VARCHAR NOT NULL, \
            book_id INTEGER REFERENCES books, \
            user_id INTEGER REFERENCES users)")

    reader = csv.reader(f)
    header = True # first line is header
    for isbn, title, author, year in reader:
        if header:
            header = False; # skip over header
        else:
            if db.execute("SELECT * FROM authors WHERE author = :author",
                    {"author": author}).rowcount == 0: # author is not yet in table authors
                db.execute("INSERT INTO authors (author) VALUES (:author)", {"author": author})
            author_id = db.execute("SELECT id FROM authors WHERE author = :author",
                    {"author": author}).fetchone()[0]
            print("author = ", author)
            print("author_id = ", author_id)
            db.execute("INSERT INTO books (isbn, title, author_id, year) VALUES (:isbn, :title, :author_id, :year)",
                    {"isbn": isbn, "title": title, "author_id": author_id, "year": year})
            print(f"Added book {title} by {author}, written {year}, with isbn {isbn}.")
    db.commit() # this locks access to database and then starts executing
                # above commands; once completed, access to database is reopened

if __name__ == "__main__":
    main()
