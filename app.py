from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
import analyzer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    info = analyzer.start(request.get_json()['text'])
    return jsonify(result=info)