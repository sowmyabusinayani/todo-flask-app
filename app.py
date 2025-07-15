from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB if not exists
def init_db():
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()

    if request.method == 'POST':
        task_content = request.form['content']
        if task_content:
            cur.execute('INSERT INTO tasks (content) VALUES (?)', (task_content,))
            conn.commit()
        return redirect('/')

    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
