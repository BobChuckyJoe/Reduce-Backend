from flask import Flask, request
from PIL import Image

from bottle_detector import detector, run_detector
from utils import to_base64, to_img

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello"


@app.route("/detect", methods=["POST"])
def detect():
    json = request.json
    # Bad security but oh well
    if json["passphrase"] != "ligma":
        return "Incorrect passphrase"
    else:
        with open("derp", "w") as f:
            f.write(json["img_data"])
        header, data = json["img_data"].split(",", 1)

        import base64
        stuff = base64.b64decode(data)
        with open("test", "wb") as f:
            f.write(stuff)
        num_bottles, labeled_image = run_detector(detector, "test")
        Image.fromarray(labeled_image).save("labeled.png")

        with open("labeled.png", "rb") as f:
            output_data_uri = header + "," + str(base64.b64encode(f.read()), "utf-8")
        return {
            "num_bottles": num_bottles,
            "labeled_image": output_data_uri
        }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12345, ssl_context="adhoc")
