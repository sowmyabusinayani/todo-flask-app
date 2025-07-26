from flask import Flask, request, render_template, redirect
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)


# Connect to PostgreSQL (update credentials before deploy)

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
"""conn = psycopg2.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    database=os.environ.get('DB_NAME', 'task_db'),
    user=os.environ.get('DB_USER', 'postgres'),
    password=os.environ.get('DB_PASSWORD', 'postsql'),
    port=os.environ.get('DB_PORT', 5432)
)"""
"""
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT", 5432),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD")
)"""


def init_db():
    with conn.cursor() as cur:
        with open('schema.sql') as f:
            cur.execute(f.read())
        conn.commit()


@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY id")
    users = cur.fetchall()

    user_data = []
    for user in users:
        cur.execute(
            "SELECT * FROM categories WHERE user_id = %s ORDER BY id", (user[0],))
        categories = cur.fetchall()
        category_data = []
        for cat in categories:
            cur.execute(
                "SELECT * FROM tasks WHERE category_id = %s ORDER BY id", (cat[0],))
            tasks = cur.fetchall()
            category_data.append({
                'id': cat[0],
                'user_id': cat[1],
                'name': cat[2],
                'created_at': cat[3].strftime("%d/%m/%Y - %H:%M") if cat[3] else '',
                'tasks': [
                    {
                        'id': t[0],
                        'category_id': t[1],
                        'name': t[2],
                        'created_at': t[3].strftime("%d/%m/%Y - %H:%M") if t[3] else ''
                    } for t in tasks
                ]
            })
        user_data.append({
            'id': user[0],
            'name': user[1],
            'created_at': user[2].strftime("%d/%m/%Y - %H:%M") if user[2] else '',
            'categories': category_data
        })
    return render_template('index.html', users=user_data)


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name'].strip()
    if not name:
        return redirect('/')  # or flash an error message

    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM users WHERE name = %s", (name,))
        if cur.fetchone():
            return redirect('/')  # User already exists
        cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
        conn.commit()
    return redirect('/')


@app.route('/add_category/<int:user_id>', methods=['POST'])
def add_category(user_id):
    name = request.form['category'].strip()
    if not name:
        return redirect('/')
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM categories WHERE user_id = %s AND name = %s", (user_id, name))
    if cur.fetchone():
        return redirect('/')  # prevent duplicates
    cur.execute(
        "INSERT INTO categories (user_id, name) VALUES (%s, %s)", (user_id, name))
    conn.commit()
    cur.close()
    return redirect('/')


@app.route('/add_task/<int:category_id>', methods=['POST'])
def add_task(category_id):
    name = request.form['task'].strip()
    if not name:
        return redirect('/')
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM tasks WHERE category_id = %s AND name = %s", (category_id, name))
    if cur.fetchone():
        return redirect('/')
    cur.execute(
        "INSERT INTO tasks (category_id, name) VALUES (%s, %s)", (category_id, name))
    conn.commit()
    cur.close()
    return redirect('/')


@app.route('/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    new_name = request.form['new_name'].strip()
    if not new_name:
        return redirect('/')
    with conn.cursor() as cur:
        cur.execute("UPDATE users SET name = %s WHERE id = %s",
                    (new_name, user_id))
        conn.commit()
    return redirect('/')


@app.route('/edit_category/<int:cat_id>', methods=['POST'])
def edit_category(cat_id):
    new_name = request.form['new_name'].strip()
    if not new_name:
        return redirect('/')
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM categories WHERE name = %s AND id != %s", (new_name, cat_id))
    if cur.fetchone():
        return redirect('/')
    cur.execute("UPDATE categories SET name = %s WHERE id = %s",
                (new_name, cat_id))
    conn.commit()
    cur.close()
    return redirect('/')


@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    new_name = request.form['new_name'].strip()
    if not new_name:
        return redirect('/')
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM tasks WHERE name = %s AND id != %s",
                (new_name, task_id))
    if cur.fetchone():
        return redirect('/')
    cur.execute("UPDATE tasks SET name = %s WHERE id = %s",
                (new_name, task_id))
    conn.commit()
    cur.close()
    return redirect('/')


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM tasks WHERE category_id IN (SELECT id FROM categories WHERE user_id = %s)", (user_id,))
    cur.execute("DELETE FROM categories WHERE user_id = %s", (user_id,))
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    return redirect('/')


@app.route('/delete_category/<int:cat_id>')
def delete_category(cat_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE category_id = %s", (cat_id,))
    cur.execute("DELETE FROM categories WHERE id = %s", (cat_id,))
    conn.commit()
    cur.close()
    return redirect('/')


@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    return redirect('/')


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
