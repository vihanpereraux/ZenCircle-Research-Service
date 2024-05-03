from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import time


app = Flask(__name__)
CORS(app)


# test route
@app.route("/", methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'}), 201


# 
@app.route("/process_eeg_data", methods=['GET'])
def process_stream_data():
    file_path = 'E:\Dev\ZenCircle\ZenCircle-Research-Service\Model\eeg_processor.py'
    
    # Number of times you want to run the script    
    number_of_runs = 1
    for _ in range(number_of_runs):
        subprocess.run(['E:\Dev\ZenCircle\ZenCircle-Research-Service\.venv\Scripts\python.exe', file_path])
    return jsonify({ 'message': 'Service file executed' }), 201

if __name__ == '__main__':
    app.run(debug=True, port=5001)
