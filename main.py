from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/signup", methods= ["POST"])
def sign_up():
    json = request.json
    print(json)
    


    return {
        "ok": "true"
    }


if __name__ == "__main__":
    cert_path = "/home/ubuntu/.monke/fullchain.pem"
    privatekey_path = "/home/ubuntu/.monke/privkey.pem"

    app.run(host="0.0.0.0", port=6969, ssl_context=(cert_path, privatekey_path))
