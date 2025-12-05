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

        # Validate input
        if not content or "id" not in content or "name" not in content:
            return jsonify({"error": "Missing 'id' or 'name' in request"}), 400

        id = content["id"]
        name = content["name"]

        data = {"id": id, "name": name}

        # Insert and ignore the result object
        collection.insert_one(data)

        # Return only the clean dict (without ObjectId)
        return jsonify({
            "message": "Data added successfully",
            "data": {"id": id, "name": name}
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get', methods=['GET'])
def get_data():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)