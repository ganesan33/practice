from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection
url = os.getenv("MONGO_URL")
client = MongoClient(url)
db = client["practice"]
collection = db["devops"]

@app.route('/')
def home():
    data = list(collection.find({}, {"_id": 0}))
    return render_template('hello.html', data=data)

@app.route('/add', methods=['POST'])
def add_data():
    try:
        content = request.get_json()  # get JSON body safely
        if not content:
            return jsonify({"error": "JSON body required"}), 400

        id = content.get("id")
        name = content.get("name")

        if id is None or name is None:
            return jsonify({"error": "Both 'id' and 'name' are required"}), 400

        data = {"id": id, "name": name}
        collection.insert_one(data)

        return jsonify({"message": "Data added successfully", "data": data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get', methods=['GET'])
def get_data():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
