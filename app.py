from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'devsecops-insecure-secret'  # intentionally weak for demo
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DB_PATH = os.path.join(BASE_DIR, 'app.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        is_admin INTEGER DEFAULT 0
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS docs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
    ''')
    # Seed a demo admin user (weak password stored in plaintext)
    try:
        cur.execute("INSERT INTO users (username, password, is_admin) VALUES ('admin', 'admin', 1)")
    except Exception:
        pass
    cur.execute("INSERT OR IGNORE INTO docs (title, content) VALUES ('Welcome', 'This is a demo document.')")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        # Intentionally weak password handling: storing plaintext
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES ('%s', '%s')" % (username, password))
            conn.commit()
            flash('Registered successfully. You can log in now.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Registration failed: ' + str(e), 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        # Intentionally vulnerable to SQL injection by concatenating strings
        query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
        cur.execute(query)
        user = cur.fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin'])
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM docs')
    docs = cur.fetchall()
    conn.close()
    return render_template('dashboard.html', docs=docs)

@app.route('/admin')
def admin():
    # Very simple admin check: username == 'admin' or is_admin flag
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Admin access required', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    conn.close()
    return render_template('admin.html', users=users)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        f = request.files.get('file')
        if not f:
            flash('No file provided', 'danger')
            return redirect(url_for('upload'))
        filename = secure_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(path)
        flash('File uploaded: ' + filename, 'success')
        return redirect(url_for('dashboard'))
    return render_template('upload.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    q = ''
    if request.method == 'POST':
        q = request.form.get('q', '')
        # Vulnerable search: direct string interpolation
        conn = get_db()
        cur = conn.cursor()
        sql = "SELECT * FROM docs WHERE title LIKE '%" + q + "%' OR content LIKE '%" + q + "%'"
        cur.execute(sql)
        results = cur.fetchall()
        conn.close()
    return render_template('search.html', results=results, q=q)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
