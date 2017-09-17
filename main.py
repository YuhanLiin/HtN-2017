from symbols import Novel
import os

from flask import Flask
app = Flask(__name__)

dir = os.path.dirname(os.path.realpath(__file__))

@app.route("/")
def index():
    with open(os.path.join(dir, 'templates', 'index.html')) as html:
        return html.read()

@app.route("/api")
def api():
    return Novel.generate()