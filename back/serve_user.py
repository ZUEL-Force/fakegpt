import hashlib
import random
import time
from flask import jsonify
from config import ALLOWED_EXTENSIONS


def get_salt(margin: int = 64):
    alphabet = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789@$#%_?'
    salt = ''
    length = len(alphabet) - 1
    for i in range(0, margin):
        salt += alphabet[random.randint(0, length)]
    return salt


def get_hash(psw: str, salt: str):
    result = psw + salt
    return hashlib.sha256(result.encode('utf-8')).hexdigest()


def wrong(msg: str, how: int = 1):
    ans = {"msg": msg, "state": how}
    return jsonify(ans)


def right(msg: str):
    ans = {"msg": msg, "state": 0}
    return jsonify(ans)


def get_time():
    return int(time.time())


def img_allowed(filename: str):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rename_img(name: str, id: int):
    fname = name.rsplit('.', 1)[1].lower()
    fname = f'{id}.' + fname
    return fname
