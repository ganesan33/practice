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
        content = request.get_json()   # read JSON body

        id = content["id"]
        name = content["name"]

        data = {"id": id, "name": name}

        collection.insert_one(data)

        # DO NOT RETURN ObjectId → only return your clean dict
        return jsonify({
            "message": "Data added successfully",
            "data": data
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get', methods=['GET'])
def get_data():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
