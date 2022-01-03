from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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


@app.route('/')
def home():
    if request.args.get("id"):
        delete_id = request.args.get("id")
        delete_book = Book.query.get(delete_id)
        db.session.delete(delete_book)
        db.session.commit()
        return redirect(url_for("home"))
    books = db.session.query(Book).all()
    return render_template("index.html", books=books)


@app.route("/edit", methods=["GET", "POST"])
def update_rating():
    if request.method == "POST":
        book_id = request.form["post_id"]
        update_book = Book.query.get(book_id)
        update_book.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for("home"))

    get_id = request.args.get("post_id")
    book_selected = Book.query.get(get_id)
    return render_template("update.html", book=book_selected)


@app.route("/add", methods=['GET', 'POST'])
def add():
    try:
        if request.method == 'POST':
            all_books.append(dict(request.form))
            new_book = Book(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for("home"))
    except:
        return redirect(url_for("home"))
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
