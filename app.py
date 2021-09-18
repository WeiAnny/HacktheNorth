from flask import *
app = Flask(__name__)

@app.route('/', methods = ['POST'])
def homepage():
    if request.method == 'POST':
        form = request.form #json format? ish
        stock = form['stock'] #id in html
        
    pass

