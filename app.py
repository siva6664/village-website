from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = 'village.db'

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            occupation TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call this on import so Gunicorn runs it too
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        occupation = request.form['occupation']
        age = request.form['age']
        gender = request.form['gender']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO people (name, occupation, age, gender) VALUES (?, ?, ?, ?)',
                       (name, occupation, age, gender))
        conn.commit()
        conn.close()
        return redirect('/list')

    return render_template('add_person.html')

@app.route('/list')
def list_people():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, occupation, age, gender FROM people')
    people = cursor.fetchall()
    conn.close()
    return render_template('list_people.html', people=people)

# No need to call app.run() if using gunicorn
