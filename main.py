from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/signup", methods= ["POST"])
def sign_up():
    pass

