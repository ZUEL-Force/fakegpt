from my_basic import db
from private import MY_QQ_ID


class QQ_MSG(db.Model):
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


def get_pre_msgs(msg: QQ_MSG):
    '''
    以满足gpt上下文要求的格式，返回指定用户的近3min聊天记录
    '''
    group_id = msg.group_id
    user_id = msg.from_id
    msg_t = msg.tstamp

    all_pre = QQ_MSG.query.filter(QQ_MSG.tstamp.__ge__(msg_t)).all()

    pre_chat = []
    for it in all_pre:
        if it.tstamp >= msg_t:
            break
        if it.from_id == MY_QQ_ID:
            if it.to_id == user_id:
                if it.group_id == group_id:
                    pre_chat.append({"role": "assistant", "content": it.text})
        if it.to_id == MY_QQ_ID:
            if it.from_id == user_id:
                if it.group_id == group_id:
                    pre_chat.append({"role": "user", "content": it.text})
    return pre_chat
