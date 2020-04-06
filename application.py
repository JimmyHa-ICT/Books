import os

import requests
from flask import Flask, session, render_template, request, url_for, redirect, jsonify
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
    if "name" in session:
        return render_template("index.html")
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", button="Log in", title="Log In", message="")
    else:
        username = request.form.get("username")
        password = request.form.get("pass")
        user = db.execute("SELECT * FROM users WHERE username=:username AND password=:password",
                             {"username": username, "password": password}).fetchone()
        if user is None:
            return render_template("login.html", button="Log in", title="Log In",
                                 message="Username or password is not correct. Please try again!")
        session["name"] = username
        return redirect(url_for("index"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("login.html", button="Sign up", title="Sign up")
    else:
        username = request.form.get("username")
        password = request.form.get("pass")
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                    {"username": username, "password": password})
        db.commit()
        return redirect(url_for("login", button="Log in", title="Log In",
                                message="Sign up successfully!"))

@app.route("/logout")
def logout():
    session.pop("name", None)
    return redirect(url_for("login"))


@app.route("/results", methods=["POST"])
def result():
    key = request.form.get("search")
    key = '%' + key + '%'
    books = db.execute("SELECT * FROM books WHERE (title LIKE :key) OR (author LIKE :key) OR (isbn LIKE :key)",
                        {"key": key}).fetchall()
    return render_template("result.html", books=books)

@app.route("/book/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
    if "name" in session:
        book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
        user = db.execute("SELECT * FROM users WHERE username=:name",
                            {"name": session["name"]}).fetchone()
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                            params={"key": "1TS2UgcLliaACF7PlaM0HQ", "isbns": isbn})
        goodreads = res.json()
        average_rating = goodreads['books'][0]['average_rating']
        work_ratings_count = goodreads['books'][0]['work_ratings_count']

        if request.method == "POST":
            rating = request.form.get("rating")
            comment = request.form.get("review")

            db.execute("INSERT INTO ratings (rating, comment, book_id, user_id) VALUES (:rating, :comment, :book_id, :user_id)",
                        {"rating": rating, "comment": comment, "book_id": book.id, "user_id": user.id})
            db.commit()
        reviews = db.execute("SELECT * FROM ratings WHERE book_id=:id", {"id": book.id}).fetchall()
        return render_template("book.html", book=book, average_rating=average_rating,
                                    work_ratings_count=work_ratings_count, reviews=reviews)

@app.route("/api/<string:isbn>")
def api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"error": "isbn is not match"})
    review_count = db.execute("SELECT COUNT(*) FROM ratings WHERE book_id = :id", {"id": book.id}).fetchone()
    average_score = db.execute("SELECT AVG(rating) FROM ratings WHERE book_id = :id", {"id": book.id}).fetchone()
    
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": isbn,
        "review_count": review_count.count,
        "average_score": average_score.avg
    })
    
    

    

