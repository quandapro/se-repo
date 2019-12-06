from flask import Flask,render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route('/signin')
@app.route("/about")
@app.route('/service')
@app.route("/")
if __name__ == "__main__":
    app.run(port= 8080)