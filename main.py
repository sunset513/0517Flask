from flask import Flask, request, render_template,url_for,redirect,g,session
from datetime import datetime


import sqlite3

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('users.db')
        db.row_factory = sqlite3.Row
    return db

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
          cursor.execute('SELECT * FROM teachers WHERE name = ? AND password = ?', (username, int(password)))
          user = cursor.fetchone()
        except ValueError:
          return 'Invalid password format'
        except sqlite3.Error as e:
          print(e)
          return f"An error occurred: {e}"
        if user:
            session['username'] = user['name']
            return redirect('/grade')
        else:
            return 'Invalid username or password'
    return render_template('index.html')

@app.route('/grade', methods=['POST', 'GET'])
def add_grade():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        score = request.form['score']
        id = request.form['student-id']
 
        try:
            cursor.execute('INSERT INTO grades (id, name, score) VALUES (?, ?, ?)', (int(id),name, score))
            conn.commit()
            return redirect('/grade')
        except Exception as e:
            print(e)
            return 'There was an issue adding your task'
    
    cursor.execute('SELECT * FROM grades ORDER BY id ASC')
    grades = cursor.fetchall()
    return render_template('grade.html', grades=grades)

## Delete grade
@app.route('/delete_grade', methods=['POST'])
def delete_grade():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        id = request.form['deleted-student-id']
        cursor.execute('DELETE FROM grades WHERE id = ?', (int(id),))
        conn.commit()
        return redirect('/grade')
    return render_template('grade.html')



if __name__ == "__main__":
  app.run(debug=True)