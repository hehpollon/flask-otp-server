from flask import Flask, request, jsonify
import pyotp
from tinydb import TinyDB, Query

app = Flask(__name__)
company_name = "flask-otp-server"

user_map = {}
db = TinyDB('./db.json')
table = db.table('users')
item = Query()


@app.route("/generate")
def generate():
    user_id = request.args.get('user_id')
    algorithm = request.args.get('algorithm')
    secret_key = pyotp.random_base32()
    if _check_exists(user_id):
        return jsonify(
            error="exists"
        ), 409  # conflict
    if algorithm == "totp":
        provisioning_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(user_id, issuer_name=company_name)
    elif algorithm == "hotp":
        provisioning_uri = pyotp.hotp.HOTP(secret_key).provisioning_uri(user_id, issuer_name=company_name)
    else:
        return jsonify(
            error="bad request"
        ), 400  # bad request

    _set_secret_key(user_id, secret_key, algorithm)
    return jsonify(
        secret_key=secret_key,
        provisioning_uri=provisioning_uri
    ), 200


@app.route("/verify")
def verify():
    user_id = request.args.get('user_id')
    algorithm = request.args.get('algorithm')
    otp_value = request.args.get('otp_value')
    counter = request.args.get('counter')
    if not _check_exists(user_id):
        return jsonify(
            error="user not exists"
        ), 404  # user not exists
    secret_key = _get_secret_key(user_id)
    if algorithm == "totp":
        otp = pyotp.TOTP(secret_key)
        result = otp.verify(otp_value)
    elif algorithm == "hotp":
        otp = pyotp.HOTP(secret_key)
        result = otp.verify(otp_value, counter=int(counter))
    else:
        return jsonify(
            error="bad request"
        ), 400  # bad request

    return jsonify(
        result=str(result)
    ), 200


def _get_secret_key(user_id):
    res = table.search(item.id == user_id)
    return res[0]['key']


def _check_exists(user_id):
    res = table.search(item.id == user_id)
    return True if res else False


def _set_secret_key(user_id, secret_key, otp_type):
    table.insert({'id': user_id, 'key': secret_key, 'type': otp_type})


if __name__ == "__main__":
    app.run(ssl_context='adhoc')  # https support
