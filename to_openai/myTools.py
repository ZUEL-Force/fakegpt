import hashlib
import json
import random
import time

# from api_openai import chatgpt_stream
import api_openai
from flask import jsonify
from mybasic import app


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


def wrong(msg: str = 'false', how: int = 1):
    ans = {"msg": msg, "state": how}
    return jsonify(ans)


def right(msg: str = 'ok'):
    ans = {"msg": msg, "state": 0}
    return jsonify(ans)


def get_time():
    return int(time.time())


def get_stream(que: list):
    i = 0
    temp = ""
    for ans in api_openai.chatgpt_stream(que):
        temp += ans
        result = {"state": 0, "msg": {"result": temp}}
        data = json.dumps(result)
        if i != 0:
            data = '\n' + data
        i += 1
        yield data
