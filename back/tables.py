from config import MY_PIC
from mybasic import db


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
    text = db.Column(db.String(4096), nullable=False)
    reason = db.Column(db.String(32), nullable=False)
    cost = db.Column(db.Integer, nullable=False)

    def __init__(self, fid: int, tid: int, tstamp: str, text: str, reason: str,
                 cost: int):
        self.from_id = fid
        self.to_id = tid
        self.tstamp = tstamp
        self.text = text
        self.reason = reason
        self.cost = cost


class QQ_temp(db.Model):
    __tablename__ = 'qq_temp'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_id = db.Column(db.Integer, nullable=False)
    to_id = db.Column(db.Integer, nullable=False)
    tstamp = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(4096), nullable=False)
    reason = db.Column(db.String(32))
    cost = db.Column(db.Integer)

    def __init__(self, fid: int, tid: int, tstamp: int, text: str, reason: str,
                 cost: int):
        self.from_id = fid
        self.to_id = tid
        self.tstamp = tstamp
        self.text = text
        self.reason = reason
        self.cost = cost

    def __init__(self, fid: int, tid: int, tstamp: int, text: str):
        self.from_id = fid
        self.to_id = tid
        self.tstamp = tstamp
        self.text = text
