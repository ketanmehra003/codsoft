from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.contact_book
contacts = db.contacts

@app.route('/')
def index():
    contact_list = contacts.find()
    return render_template('index.html', contacts=contact_list)

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        contacts.insert_one({'name': name, 'phone': phone, 'email': email, 'address': address})
        return redirect(url_for('index'))
    return render_template('add_contact.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    results = contacts.find({'$or': [{'name': {'$regex': query, '$options': 'i'}}, {'phone': {'$regex': query, '$options': 'i'}}]})
    return render_template('index.html', contacts=results)

@app.route('/update_contact/<contact_id>', methods=['GET', 'POST'])
def update_contact(contact_id):
    contact = contacts.find_one({'_id': ObjectId(contact_id)})
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        contacts.update_one({'_id': ObjectId(contact_id)}, {'$set': {'name': name, 'phone': phone, 'email': email, 'address': address}})
        return redirect(url_for('index'))
    return render_template('update_contact.html', contact=contact)

@app.route('/delete_contact/<contact_id>', methods=['GET'])
def delete_contact(contact_id):
    contacts.delete_one({'_id': ObjectId(contact_id)})
    return redirect(url_for('index'))