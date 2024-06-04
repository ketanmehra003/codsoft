from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "a2V0YW5pc2dlbml1cw=="

client = MongoClient('mongodb://localhost:27017/')
db = client['todo']

users_collection = db['users']
todos_collection = db['todos']

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
@login_required
def index():
    username = session['username']
    todos = todos_collection.find({'username': username})
    return render_template('index.html', todos=todos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            return 'Username already exists'
        else:
            hashed_password = generate_password_hash(password)
            users_collection.insert_one({'username': username, 'password': hashed_password, 'upload_id': None})
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
@login_required
def add_todo():
    username = session['username']
    todo_item = request.form.get('todo')
    todos_collection.insert_one({'username': username, 'text': todo_item, 'complete': False})
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_todo(id):
    username = session['username']
    todo = todos_collection.find_one({'_id': ObjectId(id), 'username': username})

    if request.method == 'POST':
        new_text = request.form.get('todo')
        todos_collection.update_one({'_id': ObjectId(id), 'username': username}, {'$set': {'text': new_text}})
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo)

@app.route('/complete/<id>')
@login_required
def complete_todo(id):
    todos_collection.update_one({'_id': ObjectId(id), 'username': session['username']}, {'$set': {'complete': True}})
    return redirect(url_for('index'))

@app.route('/delete/<id>')
@login_required
def delete_todo(id):
    todos_collection.delete_one({'_id': ObjectId(id), 'username': session['username']})
    return redirect(url_for('index'))