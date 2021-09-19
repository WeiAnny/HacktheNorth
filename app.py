from flask import *
app = Flask(__name__)

@app.route('/', methods = ['POST'])
def homepage():
    if request.method == 'POST':
        form = request.form #json format? ish
        stock = form['stock'] #id in html
    return render_template('index.html')

if __name__ == "__main__"
    app.run(debug = True)
