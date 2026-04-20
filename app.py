from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

#data create
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'students.db')

def init_db():
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 email TEXT,
                 course TEXT)''')
    conn.close()

print("DB Path:", db_path)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']

    conn = sqlite3.connect(db_path)
    print("DB created successfully")
    conn.execute("INSERT INTO students (name, email , course) VALUES (? , ?, ?)",
            (name,email,course))
    conn.commit()
    conn.close()

    return redirect('/display')

@app.route('/display')
def display():
    conn = sqlite3.connect(db_path)
    data = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template('display.html',data=data)
@app.route('/delete_all')
def delete_all():
    conn = sqlite3.connect(db_path)
    conn.execute("DELETE FROM students")
    conn.execute("DELETE FROM sqlite_sequence WHERE name='students'")
    conn.commit()
    conn.close()
    return redirect('/display')

if __name__ == "__main__":
   init_db()
   app.run(debug=True)