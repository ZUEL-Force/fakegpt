from flask_apscheduler import APScheduler
import threading

from my_extension import *
from my_class import MessageQueue, TEMP_MSG
from my_tables import db, QQ_MSG
from my_basic import app
from my_tools import check_key, get_time

sched = APScheduler()

Receive_Queue = MessageQueue()
Send_Queue = MessageQueue()


def send_msg():
    '''
    将gpt的回答发送到对应的好友/群聊，并将回复的答案保存至数据库
    '''
    global Send_Queue
    msg = Send_Queue.get()
    if msg == None:
        return

    ans = msg.text
    group_id = msg.group_id
    to_id = msg.to_id
    if group_id == -1:
        qq_send = {"group_id": group_id, "message": ans}
        requests.post(url=QQ_GROUP_URL, json=qq_send)
    else:
        qq_send = {"user_id": to_id, "message": ans}
        requests.post(url=QQ_PRITE_URL, json=qq_send)

    qq_msg = QQ_MSG(msg)
    with app.app_context():
        db.session.add(qq_msg)
        db.session.commit()


def check_send():
    '''
    如果待发送队列还有待发送的消息,则创建一个消息发送线程
    '''
    global Send_Queue
    while not Send_Queue.empty():
        send_thread = threading.Thread(target=send_msg())
        send_thread.start()


def get_ans():
    '''
    取一条用户的对话，并生成相应回复，将回复插入待发送队列
    '''
    global Receive_Queue, Send_Queue
    msg = Receive_Queue.get()
    if msg == None:
        return

    text, gid = msg.text, msg.group_id
    scode = check_key(text)
    ans = '后台服务超时，请稍后再试。'
    if scode == 0:
        ans = do_talk(text,msg)
    elif scode == 1:
        ans = do_help()
    elif scode == 2:
        if gid == -1:
            ans = "该功能需要在群聊中使用。"
        else:
            ans = do_ban(text, str(gid))
    elif scode == 3:
        ans = do_pic(text)
    elif scode == 5:
        ans = do_alter_audio(text)
    elif scode == 6:
        ans = do_repeat(text)
    elif scode == 7:
        ans = do_emotion()
    elif scode == 8:
        ans = do_neteasy_music()
    elif scode == 9:
        ans = do_baike(text)
    elif scode == 10:
        ans = do_searchs(text)
    elif scode == 11:
        ans = do_weather(text)
    elif scode == 12:
        ans = do_clear_sing(text)
    elif scode == 13:
        ans = do_sing(text)

    fid, tid = msg.to_id, msg.from_id
    mytime = get_time()
    qq_ans = TEMP_MSG(fid, tid, mytime, ans, gid)
    Send_Queue.put(qq_ans)


def check_receive():
    '''
    如果消息队列还有待gpt回复的消息,则创建一个生成回答线程
    '''
    global Receive_Queue
    while not Receive_Queue.empty():
        ask_thread = threading.Thread(target=get_ans())
        ask_thread.start()
