import hashlib
import requests
import random
import time

from flask import jsonify
from mybasic import app, db
from private import *


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


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


def check_key(msg: str):
    for it in SERVE_QQ_CODE.keys():
        if it in msg:
            return SERVE_QQ_CODE[it]
    return 0


def get_que_key(msg: str):
    sys_msg = {"role": "system", "content": SYSTEM_MSG}
    user_que = {"role": "user", "content": msg}
    my_chat = [sys_msg, user_que]
    to_chat = {"messages": my_chat}
    ans = requests.post(url=GPT_URL, json=to_chat).json()
    if ans['state'] == 0:
        text = str(ans['msg']['result'])
        keys = text.split(' ')
        return keys
    return []


def to_baike(bk_key: str):
    param = {'appid': BAIKE_ID, 'bk_key': bk_key}
    try:
        responce = dict(requests.get(BAIDU_BAIKE, params=param).json())
        text = responce['abstract']
        return text, 0
    except:
        return '百度百科接口超时，请稍后再试。', 1
