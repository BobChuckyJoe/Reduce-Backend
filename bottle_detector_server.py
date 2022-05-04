from flask import Flask, request

from bottle_detector import detector, run_detector
from utils import to_base64, to_img

app = Flask(__name__)


@app.route("/detect")
def detect():
    json = request.json
    # Bad security but oh well
    if json["passphrase"] != "ligma":
        return "Incorrect passphrase"
    else:
        img = to_img(json["img_data"])
        with open("test.jpg", "wb") as f:
            img.save(f)
        num_bottles, labeled_image = run_detector(detector, "test.jpg")

        return {
            "num_bottles": num_bottles,
            "labeled_image": to_base64(labeled_image)
        }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12345, ssl_context="adhoc")
