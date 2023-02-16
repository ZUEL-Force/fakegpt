from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os
import config
from config import MY_WRONG, MY_PIC, UPLOAD_FOLDER
import ai_gpt3
from serve_user import wrong, right, get_hash, get_salt, get_time, img_allowed, rename_img

app = Flask(__name__)
app.config.from_object(config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)


class User(db.Model):
    # 定义表名
    __tablename__ = 'user'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    psw = db.Column(db.String(512), nullable=False)
    salt = db.Column(db.String(256), nullable=False)
    img = db.Column(db.String(16), default=MY_PIC)

    def __init__(self, name: str, psw: str, salt: str):
        self.name = name
        self.psw = psw
        self.salt = salt
        # self.id = id


class Cookie(db.Model):
    __tablename__ = 'cookie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.Integer, nullable=False)
    uname = db.Column(db.String(64), nullable=False)
    over = db.Column(db.String(16), nullable=False)
    token = db.Column(db.String(128), nullable=False)

    def __init__(self, uuid: int, uname: str, over: str, token: str):
        self.uuid = uuid
        self.over = over
        self.token = token
        self.uname = uname


class Talk(db.Model):
    __tablename__ = 'talk'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_id = db.Column(db.Integer, nullable=False)
    to_id = db.Column(db.Integer, nullable=False)
    tstamp = db.Column(db.String(16), nullable=False)
    text = db.Column(db.String(2048), nullable=False)

    def __init__(self, fid: int, tid: int, tstamp: str, text: str):
        self.from_id = fid
        self.to_id = tid
        self.tstamp = tstamp
        self.text = text


def check_login(uid: int, token: str):
    cookies = Cookie.query.filter_by(token=token).all()
    for it in cookies:
        if uid == it.uuid:
            now = get_time()
            if now <= int(it.over):
                return True
    return False


@app.route('/talk/', methods=['POST'])
def talk():
    try:
        ans = {}
        data = request.get_data()
        js = json.loads(data)
        ctoken = js['token']
        cid = int(js['id'])
        if cid == None or ctoken == None or (not check_login(cid, ctoken)):
            return wrong("You are not logged in", 2)

        que = js['question']
        ans["answer"], ans["from"] = ai_gpt3.ask(que)
        ans["time"] = get_time()
        ans["to"] = js['from']
        talks = [
            Talk(cid, -1, str(js['time']), que),
            Talk(-1, cid, str(ans['time']), ans['answer'])
        ]
        with app.app_context():
            db.session.add_all(talks)
            db.session.commit()
        return right(ans)
    except:
        db.session.rollback()
        return wrong(MY_WRONG)


@app.route('/login/', methods=['POST'])
def login():
    try:
        ans = {}
        data = request.get_data()
        js = json.loads(data)
        #检查账号密码是否匹配
        user_name = str(js['name'])
        psw = str(js['password'])
        user = User.query.filter_by(name=user_name).first()
        if user == None:
            return wrong("Wrong name or password")
        result = get_hash(psw, user.salt)
        if user.psw != result:
            return wrong("Wrong name or password")

        #账号密码匹配后
        token = get_salt(16)
        cookie = Cookie(user.id, user.name, str(get_time() + 999 * 999), token)
        ans['token'] = token
        ans['id'] = user.id
        with app.app_context():
            db.session.add(cookie)
            db.session.commit()
        return right(ans)
    except:
        db.session.rollback()
        return wrong(MY_WRONG)


@app.route('/create/', methods=['POST'])
def create():
    try:
        user_name = request.form['name']
        psw = request.form['password']

        salt = get_salt()
        result = get_hash(psw, salt)
        user_list = User.query.filter_by(name=user_name).all()
        if len(user_list) != 0:
            return wrong("The user_name has been occupied by another user")
        if len(psw) < 6:
            return wrong("Too short password")
        #注册合法后
        user = User(user_name, result, salt)
        uid = len(User.query.all()) + 1
        if 'img' in request.files:
            file = request.files['img']
            fname = rename_img(file.filename, uid)
            user.img = fname
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))

        with app.app_context():
            db.session.add(user)
            db.session.commit()
        return right("success")
    except:
        db.session.rollback()
        return wrong(MY_WRONG)


@app.route('/getface/', methods=['POST'])
def getface():
    try:
        data = request.get_data()
        js = json.loads(data)
        ctoken = js['token']
        cid = int(js['id'])
        if cid == None or ctoken == None or (not check_login(cid, ctoken)):
            return wrong("You are not logged in", 2)

        fname = User.query.filter_by(id=cid).first().img
        # send_from_directory:使用send_file函数，将指定上传目录中的文件发送到客户端
        return send_from_directory(app.config['UPLOAD_FOLDER'], fname)
    except:
        return wrong(MY_WRONG)


@app.route('/updateface/', methods=['POST'])
def updateface():
    try:
        if 'img' not in request.files:
            return wrong("Please upload pictures.")
        file = request.files['img']
        cid = int(request.form['id'])
        ctoken = request.form['token']
        if not check_login(cid, ctoken):
            return wrong("you are not logged in")
        if file == None or not img_allowed(file.filename):
            return wrong("Upload the file in the correct format")

        fname = rename_img(file.filename, cid)
        with app.app_context():
            user = User.query.filter_by(id=cid).first()
            user.img = fname
            db.session.commit()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))

        # send_from_directory:使用send_file函数，将指定上传目录中的文件发送到客户端
        return send_from_directory(app.config['UPLOAD_FOLDER'], fname)
    except:
        db.session.rollback()
        return wrong(MY_WRONG)


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == '__main__':
    # init_db()
    app.run(debug=True, host="0.0.0.0", port=11111)
