from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
from utils import password_util


app = Flask(__name__)


def create_connection():
    conn = sqlite3.connect('static/mydatabase.db')
    return conn


def close_connection(conn):
    conn.commit()
    conn.close()


def create_users_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT, email TEXT, password BLOB, salt BLOB)''')
    conn.commit()
    conn.close()


def check_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/movies/<int:movie_id>')
def movie_page(movie_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movies WHERE id=?", (movie_id,))
    movie_data = cursor.fetchone()
    conn.close()

    if not movie_data:
        return render_template('logged.html'), 404

    return render_template('movie_page.html', movie=movie_data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')

        salt = password_util.generate_salt()

        password = password_util.get_hashed_password(password, salt)

        conn = create_connection()
        c = conn.cursor()

        c.execute(
            "INSERT INTO users(username, email, password, salt) VALUES (?, ?, ?, ?)", (username, email, password, salt)
        )
        close_connection(conn)
        return redirect('login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        close_connection(conn)
        print(user)

        if not password_util.is_valid_password(password, user[3], user[4]):
            return "Invalid username or password"
        else:
            return redirect('logged')

    return render_template('login.html')


@app.route('/list')
def movie_list():
    return render_template("list.html")


@app.route('/logged')
def logged():
    return render_template("logged.html")


if __name__ == '__main__':
    app.run()
