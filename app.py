from flask import Flask, jsonify, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

url = os.getenv("MONGO_URL")
client = MongoClient(url)

db = client.get_database('practice')
collection = db.get_collection('devops')

@app.route('/')
def home():
    data = list(collection.find({}, {'_id': 0}))
    return render_template('hello.html', data=data)

@app.route('/status')
def status():
    return jsonify({"status": "API is running smoothly."})

@app.route('/data/<int:id>', methods=['GET'])
def hello(id):
    return jsonify(f"Hello {id} welcone to this page")

@app.route('/add/<int:id>/<name>', methods=['POST','GET'])
def add_data(id, name):
    data = {"id": id, "name": name}
    collection.insert_one(data)
    return jsonify({"message": "Data added successfully", "data": data})

@app.route('/get', methods=['GET'])
def get_data():
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
