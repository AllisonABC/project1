import os

from flask import Flask, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    """Login for Bestbooks."""

    # Get form information
    username = request.form.get("username") # may want a try-except here
    password = request.form.get("password") # may want a try-except here

    # Make sure user is in the database
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
            {"username": username, "password": password}).rowcount == 0:
        return render_template("index.html", message="No user with that username and password.")
    db.commit() # probably should use a try-except here
    # flask also supports error handing for internal server errors
    return render_template("success.html")

@app.route("/register")
def register():
    """Register for Bestbooks"""

    # Get form infomration
    username = request.form.get("username") # may want a try-except here
    password = request.form.get("password") # may want a try-except here

    # Make sure user is in the database
    if db.execute("SELECT * FROM users WHERE username = :username",
            {"username": username}).rowcount == 0:
        return render_template("register.html", message="There is already a user with that username.")
    db.commit() # probably should use a try-except here

    return render_template("success.html")
