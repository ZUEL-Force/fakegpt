from my_tools import get_time
from my_basic import db, app
from private import MY_QQ_ID
from my_tables import QQ_MSG
from qq_send import Receive_Queue
from my_class import TEMP_MSG


def push_msg(temp_msg: TEMP_MSG):
    '''
    若消息队列未满，则存入消息队列，并把消息插入数据库。
    '''
    if Receive_Queue.put(temp_msg):
        qq_msg = QQ_MSG(temp_msg)
        with app.app_context():
            db.session.add(qq_msg)
            db.session.commit()


def do_private(js: dict):
    '''
    处理私聊消息
    '''
    user_id = int(js['user_id'])
    message = js['message']
    my_time = get_time()

    qq_msg = TEMP_MSG(user_id, MY_QQ_ID, my_time, message, -1)
    push_msg(qq_msg)


def do_group(js: dict):
    '''
    处理群聊消息
    '''
    message = js['message']
    if str(MY_QQ_ID) not in message:
        return

    message = message.replace(f'[CQ:at,qq={MY_QQ_ID}]', '').strip()
    js['message'] = message
    group_id = int(js['group_id'])
    user_id = int(js['user_id'])
    my_time = get_time()

    qq_msg = TEMP_MSG(user_id, MY_QQ_ID, my_time, message, group_id)
    push_msg(qq_msg)


def do_else(js: dict):
    post_type = js['post_type']
    pass
