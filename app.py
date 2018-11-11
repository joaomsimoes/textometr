from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
import redis
import analyzer

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/')
def index():
    print('hits: ' + str(cache.incr('hits')))
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    info = analyzer.start(request.get_json()['text'])
    return jsonify(result=info)