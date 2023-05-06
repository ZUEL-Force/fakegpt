import hashlib
import random
import time

from flask import jsonify
from mybasic import app
from private import *



def get_salt(margin: int = 6):
    alphabet = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789_'
    salt = ''
    length = len(alphabet) - 1
    for i in range(0, margin):
        salt += alphabet[random.randint(0, length)]
    return salt


def get_hash(psw: str, salt: str):
    result = psw + salt
    return hashlib.sha256(result.encode('utf-8')).hexdigest()


def wrong(msg: str = 'false', how: int = 1):
    ans = {"msg": msg, "state": how}
    return jsonify(ans)


def right(msg: str = 'ok'):
    ans = {"msg": msg, "state": 0}
    return jsonify(ans)


def get_time():
    return int(time.time())
