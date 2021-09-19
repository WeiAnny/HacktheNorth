from flask import *
from stockmarketpredictingapp import *
#from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#app.config['SQLALCHEMY_DATA']

#@app.route('/', methods = ['POST'])
#def homepage():
#    if request.method == 'POST':
#        form = request.form #json format? ish
#        stock = form['stock'] #id in html
#    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def getStock():
    stock = request.form['stock'] #id in html
    startdate = request.form['startdate']
    enddate = request.form['enddate']
    return render_template('result.html', stock = stock)

@app.route('/<name>', methods = ['POST', 'GET'])
def getResult(name):
    task.content = request.form['submit']
    try:
        return redirect('/')
    except:
        return 'There was an issue returning to the home page'



if __name__ == "__main__":
    app.run()
