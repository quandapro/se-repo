
from flask import Flask, redirect, url_for, request, render_template
import werkzeug
app = Flask(__name__)

@app.route('/')
def index():
   return render_template("../HomePage.html")
@app.route('/success/<name><pas>')
def success(name,pas):
   return('welcome %s' % name + " with %s" %pas)

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nam']
      pas=request.form['pas']
      return redirect(url_for('success',name = user,pas = pas))
   else:
      user = request.args.get('nam')
      return redirect(url_for('success',name = user))


if __name__ == '__main__':
   app.run(debug = True)