from flask import Flask, jsonify,render_template
from pymongo import MongoClient
import os


app = Flask(__name__)
url = os.getenv("MONGO_URL")
client = MongoClient(url)
db = client.get_database('practice')

@app.route('/')
def home():
    return render_template('hello.html')

@app.route('/status')
def status():
    return jsonify({"status": "API is running smoothly."})

@app.route('/data/<int:id>', methods=['GET'])
def hello(id):
    return jsonify(f"Hello {id} welcone to this page")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    
    
