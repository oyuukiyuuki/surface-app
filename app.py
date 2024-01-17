import nfc
import binascii
from flask import Flask, render_template, request
from nfc.tag import Tag
import json

app = Flask(__name__)


def on_connect(tag):
    if tag and tag.TYPE == "Type3Tag":
        id_info = binascii.hexlify(tag.idm).decode().upper()
    elif tag and tag.TYPE == "Type2Tag":
        id_info = binascii.hexlify(tag.identifier).decode().upper()
    elif tag and tag.TYPE == "Type4Tag":
        id_info = binascii.hexlify(tag.identifier).decode().upper()
    else:
        id_info = None


@app.route("/")
def top():
    return render_template("top.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/nfc_info")
def get_nfc_info():
    while True:
        try:
            clf = nfc.ContactlessFrontend("usb")
            tag_info = clf.connect(rdwr={"on-connect": on_connect})
            id_info = binascii.hexlify(tag_info.identifier).decode().upper()
        except Exception as e:
            id_info = "error"
        clf.close()
        if id_info != "error":
            break
    print(id_info)
    return id_info


@app.route("/status_button", methods=["GET"])
def status_button():
    json_data = request.args.get("jsonData")
    json_data = json.loads(json_data)
    nfc_id = json_data["id"]
    return render_template("status_button.html", nfc_id=nfc_id)


if __name__ == "__main__":
    app.run(debug=True, port=5500)
