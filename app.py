# app.py
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = 'data.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        if name and email:
            with sqlite3.connect(DB) as conn:
                conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
            return redirect('/list')
    return render_template('index.html')

@app.route('/list')
def list_entries():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute('SELECT name, email FROM users')
        users = cur.fetchall()
    return render_template('list.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
