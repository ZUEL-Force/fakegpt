import json
import os

from flask import request
import requests
import re

from config import QQ_PRITE_URL, QQ_GROUP_URL, QQ_BAN_URL
from mybasic import app, db
from myTools import *
from qq_server import *
from tables import QQ_temp
from private import REMOTE_URL, MY_QQ_ID


@app.route('/myqq/', methods=['GET', 'POST'])
def myqq():
    data = request.get_data()
    js = json.loads(data)
    post_type = js['post_type']
    user_id = int(js['user_id'])

    if post_type != 'message':
        if request.get_json().get('post_type') == 'request':  # 收到请求消息
            pass
        return right("ok")

    message = js['message']
    my_time = get_time()

    if js['message_type'] == 'private':
        qq = QQ_temp(user_id, MY_QQ_ID, my_time, message, -1)

        all_list = QQ_temp.query.filter(
            QQ_temp.tstamp.__ge__(int(my_time) - 200)).all()
        msg_list = []
        for it in all_list:
            if it.from_id == MY_QQ_ID:
                if it.to_id == user_id:
                    if it.group_id == -1:
                        msg_list.append({
                            "role": "assistant",
                            "content": it.text
                        })
            if it.from_id == user_id:
                if it.to_id == MY_QQ_ID:
                    if it.group_id == -1:
                        msg_list.append({"role": "user", "content": it.text})
        msg_list.append({"role": "user", "content": message})

        chat = make_chat(msg_list)
        to_chat = {
            "from": user_id,
            "time": get_time(),
            "messages": chat,
            "id": 2,
            "token": "xue_JesAbMQxYQoq"
        }

        ans = requests.post(url=REMOTE_URL, json=to_chat).json()
        qq2 = QQ_temp(MY_QQ_ID, user_id, my_time, ans['msg']['answer'], -1)
        qq_send = {"user_id": user_id, "message": ans['msg']['answer']}
        requests.post(url=QQ_PRITE_URL, json=qq_send)
        with app.app_context():
            db.session.add(qq)
            db.session.add(qq2)
            db.session.commit()
    else:
        if str("[CQ:at,qq=%s]" % MY_QQ_ID) in message:
            if "禁言" in message:
                ban_list = re.findall(r"\[CQ:at,qq=\d+\]", message)

                if len(ban_list) != 2 or str(MY_QQ_ID) in ban_list[1]:
                    qq_send = {
                        "group_id": js['group_id'],
                        "message": "格式错误，应为'@机器人 禁言@禁言对象'",
                        "auto_escape": True,
                    }
                    requests.post(url=QQ_GROUP_URL, json=qq_send)
                    return wrong("false")

                ban_id = re.findall(r"\d+", ban_list[1])[0]
                qq_send = {
                    "group_id": js['group_id'],
                    "message": "好的，已禁言[CQ:at,qq=%s]" % ban_id,
                    # "auto_escape": True,
                }
                ban_send = {
                    "group_id": js['group_id'],
                    "user_id": ban_id,
                    "duration": 60,
                }
                requests.post(url=QQ_GROUP_URL, json=qq_send)
                requests.post(url=QQ_BAN_URL, json=ban_send)
                return right("ok")

            group_id = int(js['group_id'])
            qq = QQ_temp(user_id, MY_QQ_ID, my_time, message, group_id)

            all_list = QQ_temp.query.filter(
                QQ_temp.tstamp.__ge__(int(my_time) - 200)).all()
            msg_list = []
            for it in all_list:
                if it.from_id == MY_QQ_ID:
                    if it.to_id == user_id:
                        if it.group_id == group_id:
                            msg_list.append({
                                "role": "assistant",
                                "content": it.text
                            })
                if it.from_id == user_id:
                    if it.to_id == MY_QQ_ID:
                        if it.group_id == group_id:
                            msg_list.append({
                                "role": "user",
                                "content": it.text
                            })
            msg_list.append({"role": "user", "content": message})

            chat = make_chat(msg_list)
            to_chat = {
                "from": user_id,
                "time": get_time(),
                "messages": chat,
                "id": 2,
                "token": "xue_JesAbMQxYQoq"
            }

            ans = requests.post(url=REMOTE_URL, json=to_chat).json()
            qq2 = QQ_temp(MY_QQ_ID, user_id, my_time, ans['msg']['answer'],
                          group_id)
            qq_send = {
                "group_id": js['group_id'],
                "message": ans['msg']['answer']
            }
            requests.post(url=QQ_GROUP_URL, json=qq_send)
            with app.app_context():
                db.session.add(qq)
                db.session.add(qq2)
                db.session.commit()
    return right('ok')


# TODO: 机器人群管理、机器人上下文对话

if __name__ == '__main__':
    # init_db()
    app.run(debug=True, host="0.0.0.0", port=11112)
    # app.run(host="0.0.0.0", port=11112)
