import json
import os

from flask import request
import requests

import api_openai
from config import IMG_FOLDER, MODEL, MY_REASON, QQ_PRITE_URL, QQ_GROUP_URL, MY_QQ_ID
from mybasic import app, db
from myTools import *
from tables import Talk, User
from private import REMOTE_URL


@app.route('/talk/', methods=['POST'])
def talk():
    ans = {}
    data = request.get_data()
    js = json.loads(data)
    ctoken = js['token']
    cid = int(js['id'])
    if cid == None or ctoken == None or (not check_login(cid, ctoken)):
        return wrong("You are not logged in", 2)

    que = js['messages']
    if que == None:
        return wrong("Parameter error")
    msg = api_openai.chatgpt(que)
    text = msg[0]
    reason = msg[1]
    cost = msg[2]
    ans["time"] = get_time()
    ans["to"] = js['from']
    ans["from"] = MODEL[0]
    ans["answer"] = text
    talks = [
        Talk(cid, MODEL[1], str(js['time']), str(que), MY_REASON, cost),
        Talk(MODEL[1], cid, str(ans['time']), text, reason, cost)
    ]
    with app.app_context():
        db.session.add_all(talks)
        db.session.commit()
    return right(ans)


@app.route('/login/', methods=['POST'])
def login():
    data = request.get_data()
    js = json.loads(data)

    #检查账号密码是否匹配
    user_name = str(js['name'])
    psw = str(js['password'])
    if user_name == None or psw == None:
        return wrong("Parameter error")
    user = User.query.filter_by(name=user_name).first()
    if user == None:
        return wrong("Wrong name or password")
    result = get_hash(psw, user.salt)
    if user.psw != result:
        return wrong("Wrong name or password")

    #账号密码匹配后
    ans = do_login(user)
    return right(ans)


@app.route('/create/', methods=['POST'])
def create():
    form = request.form
    if 'name' not in form.keys() or 'password' not in form.keys():
        return wrong("Parameter error")
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
        file.save(os.path.join(IMG_FOLDER, fname))

    with app.app_context():
        db.session.add(user)
        db.session.commit()
    return right("注册成功")


@app.route('/getface/', methods=['POST'])
def getface():
    data = request.get_data()
    js = json.loads(data)
    ctoken = js['token']
    cid = int(js['id'])
    if cid == None or ctoken == None or (not check_login(cid, ctoken)):
        return wrong("You are not logged in", 2)

    fname = User.query.filter_by(id=cid).first().img
    ans = {"img": f'{IMG_FOLDER}{fname}'}
    return right(ans)


@app.route('/updateface/', methods=['POST'])
def updateface():
    if 'img' not in request.files:
        return wrong("Please upload pictures.")
    file = request.files['img']

    form = request.form
    if 'id' not in form.keys() or 'token' not in form.keys():
        return wrong("Parameter error")
    cid = int(form['id'])
    ctoken = form['token']
    if not check_login(cid, ctoken):
        return wrong("you are not logged in")
    if file == None or not img_allowed(file.filename):
        return wrong("Upload the file in the correct format")

    fname = rename_img(file.filename, cid)
    with app.app_context():
        user = User.query.filter_by(id=cid).first()
        user.img = fname
        db.session.commit()
    file.save(os.path.join(IMG_FOLDER, fname))
    return right({"img": f"{IMG_FOLDER}{fname}"})


@app.route('/myqq/', methods=['GET', 'POST'])
def myqq():
    data = request.get_data()
    js = json.loads(data)
    post_type = js['post_type']
    user_id = js['user_id']

    if post_type != 'message':
        if request.get_json().get('post_type') == 'request':  # 收到请求消息
            print("收到请求消息")
            request_type = request.get_json().get('request_type')  # group
            uid = request.get_json().get('user_id')
            flag = request.get_json().get('flag')
            comment = request.get_json().get('comment')
            if request_type == "friend":
                pass
                # 直接同意，你可以自己写逻辑判断是否通过
                # set_friend_add_request(flag, "true")
            if request_type == "group":
                print("收到群请求")
                sub_type = request.get_json().get('sub_type')
                # 两种，一种的加群(当机器人为管理员的情况下)，一种是邀请入群
                gid = request.get_json().get('group_id')
                if sub_type == "add":
                    # 如果机器人是管理员，会收到这种请求，请自行处理
                    # print("收到加群申请，不进行处理")
                    pass
                elif sub_type == "invite":
                    # 直接同意，你可以自己写逻辑判断是否通过
                    # set_group_invite_request(flag, "true")
                    pass
        return right("ok")

    message = js['message']
    chat = make_chat(message)
    js_param = {
        "from": "qq",
        "time": "1676443000",
        "messages": chat,
        "id": 2,
        "token": "xue_JesAbMQxYQoq"
    }
    if js['message_type'] == 'private':
        ans = requests.post(url=REMOTE_URL, json=js_param).json()
        qq_send = {"user_id": user_id, "message": ans['msg']['answer']}
        requests.post(url=QQ_PRITE_URL, json=qq_send)
    else:
        if str("[CQ:at,qq=%s]" % MY_QQ_ID) in message:
            ans = requests.post(url=REMOTE_URL, json=js_param).json()
            qq_send = {
                "group_id": js['group_id'],
                "message": ans['msg']['answer']
            }
            requests.post(url=QQ_GROUP_URL, json=qq_send)
    return right('ok')


# TODO: 机器人群管理、机器人上下文对话

if __name__ == '__main__':
    # init_db()
    # app.run(debug=True, host="0.0.0.0", port=11112)
    app.run(host="0.0.0.0", port=11112)
