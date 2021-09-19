from flask import *
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
def get_stock():
    stock = request.form['stock'] #id in html
    startdate = request.form['startdate']
    enddate = request.form['enddate']
    return render_template('result.html', stock = stock, startdate = startdate, enddate = enddate)

if __name__ == "__main__":
    app.run()
