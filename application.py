import os

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
   if 'username' in session:
       username = session['username']
       return render_template("index.html", username=username)
   return render_template("login.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      session['username'] = request.form['username']
      username = request.form.get("username") # may want a try-except here
      password = request.form.get("password") # may want a try-except here
      # Make sure user is in the database
      if db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
              {"username": username, "password": password}).rowcount == 0:
          return render_template("error.html", message="No user with that username and password.")
      db.commit()
      return redirect(url_for('index'))

@app.route("/logout")
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))
    #return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    """Register for Bestbooks"""

    # Get form information
    try:
        username = request.form.get("username")
        password = request.form.get("password")
    except ValueError:
        return render_template("error.html", message="There was a problem with \
                the information you entered. Please try again.")

    # Check if username is already being used in database
    if db.execute("SELECT * FROM users WHERE username = :username",
            {"username": username}).rowcount > 0:
        return render_template("error.html", message="There is already a user with that username.")
    db.commit() # probably should use a try-except here

    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": username, "password": password})
    db.commit()

    return redirect(url_for('index'))

@app.route("/search", methods=["POST"])
def search():
    isbn = request.form.get("isbn").lower()
    if isbn != "":
        matches = db.execute("SELECT books.id, isbn, title, year, author FROM books JOIN authors ON books.author_id = authors.id WHERE LOWER(isbn) LIKE :isbn",
                {"isbn": '%'+isbn+'%'}).fetchall()
        return render_template("results.html", matches=matches)
    else:
        author = request.form.get("author").lower()
        print(author)
        if author != "":
            matches = db.execute("SELECT books.id, isbn, title, year, author FROM books JOIN authors ON books.author_id = authors.id WHERE LOWER(author) LIKE :author",
                    {"author": '%'+author+'%'}).fetchall()
            return render_template("results.html", matches=matches)
        else:
            title = request.form.get("title").lower()
            if title != "":
                matches = db.execute("SELECT books.id, isbn, title, year, author FROM books JOIN authors ON books.author_id = authors.id WHERE LOWER(title) LIKE :title",
                        {"title": '%'+title+'%'}).fetchall()
                return render_template("results.html", matches=matches)
            else:
                return render_template("error.html", message="No books that match query")

@app.route("/search/<int:book_id>")
def search(book_id):
    # Make sure flight exists.
    book = db.execute("SELECT books.id, isbn, title, year, author FROM books JOIN authors ON books.author_id=authors.id WHERE books.id = :id", {"id": book_id}).fetchone()
    if book is None:
        return render_template("error.html", message="No such book.")
    print("later in book\n")
    return render_template("book.html", book=book)

@app.route("/review/<int:book_id>", methods=["POST"])
def review(book_id):
    if 'username' in session:
        username = session['username']
    print("in review")
    user_id = db.execute("SELECT id FROM users WHERE username=:username",
            {"username: username"}).fetchone()
    print("in review")
    rating = request.form.get("rating")
    review = request.form.get("review")
    db.execute("INSERT INTO reviews (rating, review, book_id, user_id) \
            VALUES (:rating, :review, :book_id, :user_id)",
            {"rating": rating, "review": review, "book_id":book_id, "user_id":user_id})

"""
@app.route("/api/<string:isbn")
def api():
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
            params={"key": "FaPR4QA2NGvLSuI9nVKw", "isbns": isbn})
    res.json()"""
