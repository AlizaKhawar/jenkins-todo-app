from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = 'todos.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT NOT NULL, done INTEGER DEFAULT 0)')
        db.commit()

@app.route('/')
def index():
    db = get_db()
    todos = db.execute('SELECT * FROM todos').fetchall()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    if task:
        with get_db() as db:
            db.execute('INSERT INTO todos (task) VALUES (?)', (task,))
            db.commit()
    return redirect('/')

@app.route('/done/<int:id>')
def mark_done(id):
    with get_db() as db:
        db.execute('UPDATE todos SET done=1 WHERE id=?', (id,))
        db.commit()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
