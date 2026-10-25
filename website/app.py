import os
import bcrypt
import pyodbc
from flask import Flask, render_template, request, redirect, session, url_for
from dotenv import load_dotenv

from db import get_connection

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("todos"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", form={}, errors={})

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    errors = {}
    if not name:
        errors["name"] = "Name is required"
    if not email:
        errors["email"] = "Email is required"
    if not password:
        errors["password"] = "Password is required"
    if not confirm:
        errors["confirm"] = "Confirm password is required"
    elif password and password != confirm:
        errors["confirm"] = "Passwords do not match"

    form = {"name": name, "email": email}

    if errors:
        return render_template("register.html", form=form, errors=errors)

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
            (email, name, password_hash),
        )
        conn.commit()

        cursor.execute("SELECT user_id, name FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
    except pyodbc.IntegrityError:
        conn.rollback()
        errors["email"] = "Email Already Exists"
        return render_template("register.html", form=form, errors=errors)
    finally:
        conn.close()

    session["user_id"] = row.user_id
    session["name"] = row.name
    return redirect(url_for("todos"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", form={}, errors={})

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    errors = {}
    if not email:
        errors["email"] = "Email is required"
    if not password:
        errors["password"] = "Password is required"

    form = {"email": email}

    if errors:
        return render_template("login.html", form=form, errors=errors)

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, name, password_hash FROM users WHERE email = ?",
            (email,),
        )
        row = cursor.fetchone()
    finally:
        conn.close()

    valid = row is not None and bcrypt.checkpw(
        password.encode("utf-8"), row.password_hash.encode("utf-8")
    )

    if not valid:
        errors["general"] = "Invalid email or password"
        return render_template("login.html", form=form, errors=errors)

    session["user_id"] = row.user_id
    session["name"] = row.name
    return redirect(url_for("todos"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def render_todos(form=None, errors=None, edit_error=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT todo_id, title, is_done, created_at FROM todos "
            "WHERE user_id = ? ORDER BY todo_id DESC",
            (session["user_id"],),
        )
        rows = cursor.fetchall()
    finally:
        conn.close()

    return render_template(
        "todos.html",
        name=session["name"],
        todos=rows,
        form=form or {},
        errors=errors or {},
        edit_error=edit_error,
    )


@app.route("/todos")
def todos():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_todos()


@app.route("/todos/add", methods=["POST"])
def add_todo():
    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title", "").strip()

    if not title:
        return render_todos({"title": title}, {"title": "Title is required"})
    if len(title) > 200:
        return render_todos({"title": title}, {"title": "Title is too long (200 characters at most)"})

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (user_id, title) VALUES (?, ?)",
            (session["user_id"], title),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("todos"))

@app.route("/todos/<int:todo_id>/edit", methods=["POST"])
def edit_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title", "").strip()

    if not title:
        return render_todos(edit_error="Title is required")
    if len(title) > 200:
        return render_todos(edit_error="Title is too long (200 characters at most)")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE todos SET title = ? WHERE todo_id = ? AND user_id = ?",
            (title, todo_id, session["user_id"]),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
def toggle_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    is_done = 1 if request.form.get("is_done") == "1" else 0

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE todos SET is_done = ? WHERE todo_id = ? AND user_id = ?",
            (is_done, todo_id, session["user_id"]),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM todos WHERE todo_id = ? AND user_id = ?",
            (todo_id, session["user_id"]),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("todos"))

def render_library(author_form=None, author_errors=None, book_form=None, book_errors=None,
                   author_edit_error=None, book_edit_error=None):
    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT author_id, name, country FROM AUTHOR ORDER BY author_id")
        authors = cursor.fetchall()
        cursor.execute("SELECT book_id, title, price, author_id FROM BOOK ORDER BY book_id")
        books = cursor.fetchall()
    finally:
        conn.close()

    return render_template(
        "library.html",
        authors=authors,
        books=books,
        author_form=author_form or {},
        author_errors=author_errors or {},
        book_form=book_form or {},
        book_errors=book_errors or {},
        author_edit_error=author_edit_error,
        book_edit_error=book_edit_error,
    )


@app.route("/library")
def library():
    return render_library()

@app.route("/library/authors/add", methods=["POST"])
def add_author():
    name = request.form.get("name", "").strip()
    country = request.form.get("country", "").strip()

    if not name:
        return render_library(
            author_form={"name": name, "country": country},
            author_errors={"name": "Name is required"},
        )
    if len(name) > 100:
        return render_library(
            author_form={"name": name, "country": country},
            author_errors={"name": "Name is too long (100 characters at most)"},
        )

    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO AUTHOR (name, country) VALUES (?, ?)",
            (name, country or None),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))

@app.route("/library/books/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    price = request.form.get("price", "").strip()
    author_id = request.form.get("author_id", "").strip()

    form = {"title": title, "price": price, "author_id": author_id}
    errors = {}

    if not title:
        errors["title"] = "Title is required"
    elif len(title) > 150:
        errors["title"] = "Title is too long (150 characters at most)"

    if not price:
        errors["price"] = "Price is required"
    else:
        try:
            if float(price) < 0:
                errors["price"] = "Price cannot be negative"
        except ValueError:
            errors["price"] = "Price must be a number"

    if not author_id:
        errors["author_id"] = "Author is required"

    if errors:
        return render_library(book_form=form, book_errors=errors)

    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO BOOK (title, price, author_id) VALUES (?, ?, ?)",
            (title, price, int(author_id)),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))

@app.route("/library/authors/<int:author_id>/edit", methods=["POST"])
def edit_author(author_id):
    name = request.form.get("name", "").strip()
    country = request.form.get("country", "").strip()

    if not name:
        return render_library(author_edit_error="Author name is required")
    if len(name) > 100:
        return render_library(author_edit_error="Author name is too long (100 characters at most)")

    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE AUTHOR SET name = ?, country = ? WHERE author_id = ?",
            (name, country or None, author_id),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))

@app.route("/library/books/<int:book_id>/edit", methods=["POST"])
def edit_book(book_id):
    title = request.form.get("title", "").strip()
    price = request.form.get("price", "").strip()
    author_id = request.form.get("author_id", "").strip()

    if not title:
        return render_library(book_edit_error="Book title is required")
    if len(title) > 150:
        return render_library(book_edit_error="Book title is too long (150 characters at most)")
    try:
        if float(price) < 0:
            return render_library(book_edit_error="Price cannot be negative")
    except ValueError:
        return render_library(book_edit_error="Price must be a number")
    if not author_id:
        return render_library(book_edit_error="Author is required")

    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE BOOK SET title = ?, price = ?, author_id = ? WHERE book_id = ?",
            (title, price, int(author_id), book_id),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))


@app.route("/library/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM BOOK WHERE book_id = ?", (book_id,))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))


@app.route("/library/authors/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM AUTHOR WHERE author_id = ?", (author_id,))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))

if __name__ == "__main__":
    app.run(debug=True)