import hashlib
import random
import time

from flask import jsonify

from config import ALLOWED_EXTENSIONS
from mybasic import app
from tables import *


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


def check_login(uid: int, token: str):
    cookies = Cookie.query.filter_by(token=token).all()
    for it in cookies:
        if uid == it.uuid:
            now = get_time()
            if now <= int(it.over):
                return True
    return False


def do_login(user: User):
    ans = {}
    token = get_salt(16)
    cookie = Cookie(user.id, user.name, str(get_time() + 999 * 999), token)
    ans['token'] = token
    ans['id'] = user.id
    with app.app_context():
        db.session.add(cookie)
        db.session.commit()
    return ans


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
