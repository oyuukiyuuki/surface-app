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
        flag = True
        print("カードをかざしてください:")
        try:
            clf = nfc.ContactlessFrontend("usb")
            tag = clf.connect(rdwr={"on-connect": lambda tag: False})
            clf.close()
            # ICカードのID情報抽出して表示する
            if tag and tag.TYPE == "Type3Tag":
                id_info = binascii.hexlify(tag.idm).decode().upper()
            elif tag and tag.TYPE == "Type2Tag":
                id_info = binascii.hexlify(tag.identifier).decode().upper()
            elif tag and tag.TYPE == "Type4Tag":
                id_info = binascii.hexlify(tag.identifier).decode().upper()
            else:
                id_info = None
        except Exception as e:
            flag = False
        if flag and not (id_info is None):
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
