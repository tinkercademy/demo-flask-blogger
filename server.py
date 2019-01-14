import flask
from flask import render_template, request, flash, redirect, url_for
import os
import sqlite3
app = flask.Flask(__name__)

def get_db():
    db = sqlite3.connect('db.sqlite3')
    db.row_factory = sqlite3.Row
    return db

def create_db():
    db = get_db()
    db.execute('CREATE TABLE post ' + \
               '(id INTEGER PRIMARY KEY AUTOINCREMENT, ' + \
               'title TEXT NOT NULL, ' + \
               'body TEXT, ' + \
               'image TEXT, ' + \
               'file TEXT)')
    db.close()

if not os.path.isfile('db.sqlite3'):
    create_db()

@app.route('/')
def index():
    db = get_db()
    posts = get_db().execute('SELECT * FROM post').fetchall()
    db.close()
    return render_template("index.html", posts=posts)

# This is a silly way to insert posts without a GUI!
@app.route('/add/<title>/<body>')
def add(title, body):
    db = get_db()
    db.execute('INSERT INTO post(title, body) VALUES (?,?)', (title,body))
    db.commit()
    db.close()
    return redirect(url_for('index'))

# Show a single post 
@app.route('/posts/<id>')
def get_post(id):
    db = get_db()
    cursor = db.execute('SELECT * from post WHERE id=?', (id))
    post = cursor.fetchone()
    db.close()
    return render_template('showpost.html', post=post)

# Create post: handle GET (show form) and POST (process form)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpost.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.run(debug=True)


