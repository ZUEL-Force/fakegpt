from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import config
import ai_gpt3
from serve_user import wrong, right, get_hash, get_salt, get_time

app = Flask(__name__)
app.config.from_object(config)
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


@app.route('/talk/', methods=['POST', 'GET'])
def talk():
    ans = {}
    try:

        data = request.get_data()
        js = json.loads(data)
        ctoken = js['token']
        cid = int(js['id'])
        if cid == None or ctoken == None or (not check_login(cid, ctoken)):
            return wrong("You are not logged in")

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
        return wrong("Background service error, please try again later")


@app.route('/login/', methods=['POST'])
def login():
    try:
        ans = {}
        cname = request.cookies.get('name')
        ctoken = request.cookies.get('token')
        if cname != None and ctoken != None and check_login(cname, ctoken):
            return wrong("you've already logged in")
        data = request.get_data()
        js = json.loads(data)
        #检查账号密码是否匹配
        user_name = str(js['name'])
        psw = str(js['password'])
        user_name.encode('utf-8')
        psw.encode('utf-8')
        user = User.query.filter_by(name=user_name).first()
        if user == None:
            return wrong("Wrong name or password")
        result = get_hash(psw, user.salt)
        if user.psw != result:
            return wrong("Wrong name or password")

        #账号密码匹配后
        token = get_salt(16)
        cookie = Cookie(user.id, user.name, str(get_time() + 3600), token)
        ans['token'] = token
        ans['id'] = user.id
        with app.app_context():
            db.session.add(cookie)
            db.session.commit()
        return right(ans)
    except:
        db.session.rollback()
        return wrong("Background service error, please try again later")


@app.route('/create/', methods=['POST'])
def create():
    try:
        data = request.get_data()
        js = json.loads(data)
        #检查用户名是否被占用
        user_name = str(js['name'])
        psw = str(js['password'])
        salt = get_salt()
        result = get_hash(psw, salt)
        user_list = User.query.filter_by(name=user_name).all()
        if len(user_list) != 0:
            return wrong("The user_name has been occupied by another user")
        if len(psw) < 6:
            return wrong("Too short password")
        #注册合法后
        user = User(user_name, result, salt)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        return right("success")
    except:
        db.session.rollback()
        return wrong("Background service error, please try again later")


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == '__main__':
    # init_db()
    # app.run(debug=True, port=8888)
    app.run(debug=True, host="0.0.0.0", port=8888)
# ?n8G5Bhk7npmWoZ0
# ?n8G5Bhk7npmWoZ0