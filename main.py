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
email_to_sess_id = dict()
sess_id_to_user = dict()


def add_sess_id(user_email):
    session_id = str(uuid.uuid4())
    email_to_sess_id[user_email] = session_id
    sess_id_to_user[session_id] = user_email


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
            password_hash = str(nacl.pwhash.str(bytes(password, "utf-8")), "utf-8")
            user = User(email, first_name, last_name, password_hash)
            add_user(user)

            add_sess_id(email)
            return {
                "ok": "true",
                "session_id": email_to_sess_id[email]
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
        user_hash = user.password_hash
        print("Login stuff")
        print(user_hash)
        print(json["password"])
        try:
            nacl.pwhash.verify(bytes(user_hash, "utf-8"), bytes(json["password"], "utf-8"))
        except InvalidkeyError:
            return {
                "ok": "false",
                "error_message": "Username or password is incorrect"
            }
        if user.email not in email_to_sess_id:
            add_sess_id(user.email)

        return {
            "ok": "true",
            "session_id": email_to_sess_id[user.email]
        }


user_stats = {
    "prev_weeks": [
        ["04/03", 840],
        ["04/10", 849],
        ["04/17", 840],
        ["04/24", 860]],
    "curr_week": {
        "bottles": 190,
        "cans": 136,
        "cups": 107,
        "paper": 216,
        "other": 200
    }
}

house_stats = {
    "prev_weeks": [
        ["04/03", 3320],
        ["04/10", 3386],
        ["04/17", 3360],
        ["04/24", 3440]],
    "curr_week": {
        "bottles": 760,
        "cans": 544,
        "cups": 428,
        "paper": 864,
        "other": 800
    },
    "members": [
        { "name": "You", "amount": 849 },
        { "name": "Jane", "amount": 870 },
        { "name": "Jack", "amount": 834 },
        { "name": "Jill", "amount": 843 }]
}

@app.route("/stats", methods=["GET"])
def stats():
    return user_stats


@app.route("/stats/increase", methods=["POST"])
def increase_stats():
    json = request.json
    trash_type = json["trash_type"]
    amount = 1
    if trash_type == "other":
        amount = json["amount"]
    user_stats["curr_week"][trash_type] += amount
    house_stats["curr_week"][trash_type] += amount
    house_stats["curr_week"][0]["amount"] += amount


@app.route("/stats/decrease", methods=["POST"])
def decrease_stats():
    json = request.json
    trash_type = json["trash_type"]
    user_stats["curr_week"][trash_type] -= 1
    house_stats["curr_week"][trash_type] -= 1
    house_stats["curr_week"][0]["amount"] -= 1


@app.route("/members")
def members():
    return house_stats


@app.route("/upload", methods=["POST"])
def post():
    # Users will post to
    json = request.json
    session_id = json["session_id"]
    print(f"User gave: {json['session_id']}")
    print(f"We have: {sess_id_to_user}")

    if session_id not in sess_id_to_user:
        return {
            "ok": "false",
            "error_message": "Bad session ID (are you logged in?)"
        }
    else:
        img = json["img"]
        # Offload the inference step (maestro is a potato)
        res = requests.post(url="https://35.175.235.213:12345/detect",
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
