from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from analyzer import Analyzer
import logging

logging.basicConfig(filename="logs.log", level=logging.INFO)

app = Flask(__name__)
logging.info('Flask app created')
analyzer_object = Analyzer()
logging.info('Analyzer object created')

@app.route('/')
def index():
    logging.info('new user ip: ' + request.remote_addr)
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.get_json()['text']
    logging.info(text)
    info = analyzer_object.start(text)
    return jsonify(result=info)