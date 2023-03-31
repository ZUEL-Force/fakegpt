from mybasic import db


class QQ_temp(db.Model):
    __tablename__ = 'qq_temp'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_id = db.Column(db.Integer, nullable=False)
    to_id = db.Column(db.Integer, nullable=False)
    tstamp = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(4096), nullable=False)
    group_id = db.Column(db.Integer, nullable=False)

    def __init__(self, fid: int, tid: int, tstamp: int, text: str, gid: int):
        self.from_id = fid
        self.to_id = tid
        self.tstamp = tstamp
        self.text = text
        self.group_id = gid
