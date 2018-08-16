from flask import Flask
from flask import render_template
import analyzer

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.info(analyzer.start('идет дождь'))
    return render_template('index.html')