from flask import Flask, request, render_template,url_for,redirect,g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import sqlite3

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('users.db')
        db.row_factory = sqlite3.Row
    return db

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
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
            cursor.execute('INSERT INTO grades (id, name, score) VALUES (?, ?, ?)', (id,name, score))
            conn.commit()
            return redirect('/grade')
        except Exception as e:
            print(e)
            return 'There was an issue adding your task'
    
    cursor.execute('SELECT * FROM grades')
    grades = cursor.fetchall()
    return render_template('grade.html', grades=grades)

## Delete grade
@app.route('/delete_grade', methods=['POST'])
def delete_grade():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        id = request.form['deleted-student-id']
        cursor.execute('DELETE FROM grades WHERE id = ?', (id,))
        conn.commit()
        return redirect('/grade')
    return render_template('grade.html')



if __name__ == "__main__":
  app.run(debug=True)