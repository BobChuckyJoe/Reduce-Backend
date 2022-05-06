import base64
from pprint import pprint
import uuid

from flask import Flask, request
from flask_cors import CORS
import nacl.pwhash
from nacl.exceptions import InvalidkeyError
import requests

from data import User
from db import get_user, add_user

app = Flask(__name__)
CORS(app)

# Users will use session ids to keep their local state
user_to_sess_id = dict()
sess_id_to_user = dict()


def add_sess_id(user):
    session_id = uuid.uuid4()
    user_to_sess_id[user] = session_id
    sess_id_to_user[session_id] = user


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/signup", methods=["POST"])
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
            password_hash = nacl.pwhash.str(bytes(password, "utf-8"))
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
            nacl.pwhash.verify(json["password"])
        except InvalidkeyError:
            return {
                "ok": "false",
                "error_message": "Username or password is incorrect"
            }
        if user not in user_to_sess_id:
            add_sess_id(user)

        return {
            "ok": "true",
            "session_id": user_to_sess_id[user]
        }


@app.route("/upload", methods=["POST"])
def post():
    # Users will post to
    json = request.json
    session_id = json["session_id"]
    if session_id not in sess_id_to_user:
        return {
            "ok": "false",
            "error_message": "Bad session ID (are you logged in?)"
        }
    else:
        img = json["img"]
        # Offload the inference step (maestro is a potato)
        res = requests.post(url="https://jalad.cs.utexas.edu:12345/detect",
                            json={
                                "passphrase": "ligma",
                                "img_data": img
                            },
                            verify=False)

        res_json = res.json()
        if res.status_code != 200:
            print("Something went wrong with post request")
            return {
                "ok": "false",
                "error_message": "Something went wrong on our end! Sorry..."
            }

        return {
            "ok": "true",
            "num_bottles": res_json["num_bottles"],
            "labeled_image": res_json["labeled_image"]
        }


@app.route("/check_sess", methods=["POST"])
def check_sess():
    json = request.json
    if json["session_id"] in sess_id_to_user:
        return {
            "ok": "true"
        }
    else:
        return {
            "ok": "false"
        }


if __name__ == "__main__":
    cert_path = "/home/ubuntu/.monke/fullchain.pem"
    privatekey_path = "/home/ubuntu/.monke/privkey.pem"

    app.run(host="0.0.0.0", port=6969, ssl_context=(cert_path, privatekey_path))
