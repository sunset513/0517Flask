from flask import Flask, request, render_template, url_for, redirect, g, session, flash
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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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
        if not username or not password:
            flash('Username and password cannot be empty', 'error')
            return redirect(url_for('index'))
        try:
            cursor.execute('SELECT * FROM teachers WHERE name = ?', (username,))
            user = cursor.fetchone()
            if user:
                if user['password'] == int(password):
                    session['username'] = user['name']
                    return redirect('/grade')
                else:
                    flash('Incorrect password', 'error')
            else:
                flash('Incorrect username', 'error')
        except sqlite3.Error as e:
            flash(f"An error occurred: {e}", 'error')
        return redirect(url_for('index'))


@app.route('/grade', methods=['POST', 'GET'])
def add_grade():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        score = request.form['score']
        student_id = request.form['student-id']
        if not name or not score or not student_id:
            flash('All fields are required', 'error')
            return redirect(url_for('add_grade'))
        try:
            cursor.execute('INSERT INTO grades (id, name, score) VALUES (?, ?, ?)', (int(student_id), name, score))
            conn.commit()
            flash('Grade added successfully', 'success')
        except sqlite3.Error as e:
            flash(f"An error occurred: {e}", 'error')
        return redirect(url_for('add_grade'))
    
    cursor.execute('SELECT * FROM grades ORDER BY id ASC')
    grades = cursor.fetchall()
    return render_template('grade.html', grades=grades)

@app.route('/delete_grade', methods=['POST'])
def delete_grade():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        student_id = request.form['deleted-student-id']
        if not student_id:
            flash('Student ID is required', 'error')
            return redirect(url_for('add_grade'))
        try:
            cursor.execute('DELETE FROM grades WHERE id = ?', (int(student_id),))
            conn.commit()
            flash('Grade deleted successfully', 'success')
        except sqlite3.Error as e:
            flash(f"An error occurred: {e}", 'error')
        return redirect(url_for('add_grade'))

if __name__ == "__main__":
    app.run(debug=True)
