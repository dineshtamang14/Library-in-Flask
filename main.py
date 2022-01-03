from crypt import methods

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from models import Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)


db.create_all()

all_books = []


@app.route("/update", methods=["GET", "POST"])
def update_rating(id: int):
    rating_to_update = Book.query.get(id)
    print(rating_to_update)
    if request.method == "GET":
        return render_template("update.html", book=rating_to_update)
    else:
        rating_to_update.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for("home"))


@app.route('/')
def home():
    books = db.session.query(Book).all()
    return render_template("index.html", books=books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        all_books.append(dict(request.form))
        new_book = Book(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

