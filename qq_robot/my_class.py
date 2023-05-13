import threading
import queue


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


class TEMP_MSG():
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
