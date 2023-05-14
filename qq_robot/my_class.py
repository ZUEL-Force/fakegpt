import threading
import queue
import sqlite3

from private import MY_QQ_ID, CREATE_QQ_MSG, INSERT_QQ_MSG, PRE_MSG_SQL, DATABASE_URI


class MessageQueue:
    def __init__(self, size=10):
        self.queue = queue.Queue(maxsize=size)
        self.lock = threading.Lock()

    def put(self, item):
        with self.lock:
            if self.queue.full():
                return False
            self.queue.put(item)
        return True

    def get(self):
        with self.lock:
            if self.queue.empty():
                return None
            item = self.queue.get()
        return item

    def full(self):
        with self.lock:
            return self.queue.full()

    def empty(self):
        with self.lock:
            return self.queue.empty()


class QQ_MSG:
    fid: int
    tid: int
    tstamp: int
    text: str
    gid: int

    def __init__(self, fid: int, tid: int, tstamp: int, text: str, gid: int):
        self.fid = fid
        self.tid = tid
        self.tstamp = tstamp
        self.text = text
        self.gid = gid


class DB_Conn:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DATABASE_URI)
        self.lock = threading.Lock()

    def execute(self, sql: str, params):
        with self.lock:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, params)

    def commit(self):
        with self.lock:
            self.conn.commit()

    def fetchall(self, sql: str, params):
        with self.lock:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, params)
            return self.cur.fetchall()

    def close(self):
        with self.lock:
            self.cur.close()


my_db = DB_Conn()


def init_db():
    tables = my_db.fetchall(
        "SELECT name FROM sqlite_master WHERE type='table'")

    for table_name in tables:
        if table_name[0] == 'sqlite_sequence':
            continue
        my_db.execute("DROP TABLE IF EXISTS " + table_name[0])

    my_db.execute(CREATE_QQ_MSG)
    my_db.close()


def insert_msg(msg: QQ_MSG):
    values = (msg.fid, msg.tid, msg.tstamp, msg.text, msg.gid)
    my_db.execute(INSERT_QQ_MSG, values)
    my_db.commit()
    my_db.close()


def pre_msg(msg: QQ_MSG):
    values = (msg.gid, msg.fid, msg.fid, msg.tstamp - 300)
    results = my_db.fetchall(PRE_MSG_SQL, values)

    pre_chat = []
    #record id,fid,tid,tstamp,text,gid
    for record in results:
        if record[1] == msg.fid and record[2] == MY_QQ_ID:
            pre_chat.append({"role": "user", "content": record[4]})
        elif record[2] == msg.fid and record[1] == MY_QQ_ID:
            pre_chat.append({"role": "assistant", "content": record[4]})

    my_db.close()
    return pre_chat
