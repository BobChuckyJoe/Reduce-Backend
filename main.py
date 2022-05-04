import base64
from pprint import pprint
import uuid

from flask import Flask, request
from flask_cors import CORS

import nacl.pwhash
from nacl.exceptions import InvalidkeyError

from data import User
from db import get_user, add_user
app = Flask(__name__)
CORS(app)

# Users will use session ids to keep their local state
sess_ids = dict()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/signup", methods= ["POST"])
def sign_up():
    json = request.json
    pprint(json)
    
    user = get_user(json["email"])
    if user is not None:
        # User exists!
        return {
            "ok": "false",
            "error_message": "An account with this email already exists!"
        }
    else:
        # Create the user here
        email = json["email"]
        first_name = json["first_name"]
        last_name = json["last_name"]
        password = json["password"]
        confirm_password = json["confirm_password"]

        if password != confirm_password:
            return {
                "ok": "false",
                "error_message": "Passwords do not match"
            }
        else:
            password_hash = nacl.pwhash.str(password)
            user = User(email, first_name, last_name, password_hash)
            add_user(user)
            session_id = str(uuid.uuid4())

            return {
                "ok": "true",
                "session_id": session_id
            }

@app.route("/login", methods=["POST"])
def login():
    json = request.json
    user = get_user(json["email"])
    if user is None:
        return {
            "ok": "false",
            "error_message": "Username or password is incorrect"
        }
    else:
        # Verify password
        try:
            nacl.pwhash.verify(user[""])
        except InvalidkeyError:
            return {
                "ok": "false",
                "error_message": "Username or password is incorrect"
            }

if __name__ == "__main__":
    cert_path = "/home/ubuntu/.monke/fullchain.pem"
    privatekey_path = "/home/ubuntu/.monke/privkey.pem"

    app.run(host="0.0.0.0", port=6969, ssl_context=(cert_path, privatekey_path))
