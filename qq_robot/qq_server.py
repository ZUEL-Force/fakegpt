import re
from io import BytesIO
from pathlib import Path
from random import randint

import requests
from my_tools import *
from mybasic import db
from PIL import Image
from private import *
from tables import QQ_temp

speaker = 'kokomi'


def do_talk(js: dict, group_id: int):
    my_time = get_time()
    user_id = int(js['user_id'])
    sys_msg = {"role": "system", "content": SYSTEM_MSG}
    message = js['message']

    all_pre = QQ_temp.query.filter(QQ_temp.tstamp.__ge__(int(my_time) -
                                                         200)).all()
    my_chat = [sys_msg]
    for it in all_pre:
        if it.from_id == MY_QQ_ID:
            if it.to_id == user_id:
                if it.group_id == group_id:
                    my_chat.append({"role": "assistant", "content": it.text})
        if it.to_id == MY_QQ_ID:
            if it.from_id == user_id:
                if it.group_id == group_id:
                    my_chat.append({"role": "user", "content": it.text})
    my_chat.append({"role": "user", "content": message})

    to_chat = {"messages": my_chat}
    ans = requests.post(url=GPT_URL, json=to_chat).json()
    if ans['state'] == 0:
        text = ans['msg']['result']
        if len(text) <= 100:
            if randint(1, 5) <= 2:
                return do_repeat({'message': text})
        return text
    return '响应超时，请稍后重试。'


def do_help(js: dict):
    return "胖熊还没写help，以后再说"


def do_ban(js: dict):
    message = js['message']
    ban_list = re.findall(r"禁言\[CQ:at,qq=\d+\]", message)

    if len(ban_list) != 1 or str(MY_QQ_ID) in ban_list[0]:
        return "格式错误，应为'@机器人 禁言@禁言对象'"

    ban_id = re.findall(r"\d+", ban_list[0])[0]
    ban_send = {
        "group_id": js['group_id'],
        "user_id": ban_id,
        "duration": 60,
    }
    requests.post(url=QQ_BAN_URL, json=ban_send)
    return "好的，已禁言[CQ:at,qq=%s]" % ban_id


def do_pic(js: dict):
    message = js['message']
    ans = requests.post(url=CREATE_IMG_URL, json={"messages": message}).json()
    if ans['state'] == 1:
        return ans['msg']['result']

    img_url = ans['msg']['result']
    res = requests.get(img_url)
    img = Image.open(BytesIO(res.content))
    img_name = get_salt(6) + '.jpg'
    img.save(IMG_ABSOLUTE + img_name)
    img_url = Path.as_uri(Path(IMG_ABSOLUTE + img_name))
    return ("[CQ:image,file=%s]" % img_url)


# def do_autio(js: dict, gid: int):
#     message = js['message']

#     i_rand = randint(0, 13)
#     return ("[CQ:record,file=%s]" % audio_url)


def do_alter_audio(js: dict):
    global speaker

    message = str(js['message'])
    message = message.replace('音色', '')
    message = message.replace('音色：', '')
    message = message.replace('音色:', '')
    message = message.strip()

    ans = requests.post(SPEAKERS_URL).json()
    sdict = ans['msg']['result']
    if message in sdict.keys():
        speaker = message
        welcome = {'message': sdict[speaker]['text']}
        return do_repeat(welcome)
    else:
        return f"切换失败，{message}音色不存在"


def do_repeat(js: dict):
    global speaker

    message = str(js['message'])
    message = message.replace('复读', '')
    message = message.replace('复读：', '')
    message = message.replace('复读:', '')
    if len(message) == 0:
        return 'E:复读内容过短'
    elif len(message) > 100:
        return '复读内容过长'

    ans = requests.post(TTS_URL, json={
        'message': message,
        'speaker': speaker
    }).json()
    if ans['state'] == 0:
        audio_url = AUDIO_REMOTE + ans['msg']['result']
        # print(audio_url)
        return ("[CQ:record,file=%s]" % audio_url)
    else:
        return ans['msg']['result']


def do_emotion():
    index = randint(0, 9)
    file_name = f'表情包{index}.jpg'
    emotion_url = Path.as_uri(Path(EMOTION_ABSOLUTE + file_name))
    return ("[CQ:image,file=%s]" % emotion_url)


def do_neteasy_music():
    choice = MUSIC_CHOICE[randint(0, len(MUSIC_CHOICE) - 1)]
    param = {'sort': choice, 'format': 'json'}
    try:
        responce = requests.get(NET_EASY_MUSIC, params=param)
        responce.raise_for_status()
        responce.encoding = responce.apparent_encoding
        text = responce.text
        if 'id' in text:
            pattern = r'id=(\d+)'
            match = re.search(pattern, text)
            if match:
                music_id = int(match.group(1))
                return f'[CQ:music,type=163,id={music_id}]'
        return '点歌失败，请稍后重试。'
    except:
        return '点歌失败，请稍后重试。'


def do_baike(js: dict):
    msg = str(js['message'])
    msg = msg.replace('百度', '')
    msg = msg.replace('百科', '')
    msg = msg.strip()
    if len(msg) > 10:
        return '搜索内容过长。'
    res, state = to_baike(msg)
    return res


def do_searchs(js: dict):
    sys_msg = {"role": "system", "content": SYSTEM_MSG}
    my_chat = [sys_msg]

    msg = str(js['message'])
    keys = get_que_key(msg)
    for key in keys:
        text, state = to_baike(key)
        if state == 0:
            user_msg = {"role": "user", "content": text}
            my_chat.append(user_msg)
    my_chat.append({"role": "user", "content": text})
    to_chat = {"messages": my_chat}
    ans = requests.post(url=GPT_URL, json=to_chat).json()
    if ans['state'] == 0:
        text = str(ans['msg']['result'])
        return text
    return '后台服务超时，请稍后再试。'


def get_ans(js: dict, gid: int):
    scode = check_key(js['message'])
    ans = '后台服务超时，请稍后再试'
    if scode == 0:
        ans = do_talk(js, gid)
    elif scode == 1:
        ans = do_help(js)
    elif scode == 2:
        if gid == -1:
            ans = "该功能需要在群聊中使用。"
        else:
            ans = do_ban(js)
    elif scode == 3:
        ans = do_pic(js)
    elif scode == 5:
        ans = do_alter_audio(js)
    elif scode == 6:
        ans = do_repeat(js)
    # elif scode == 4:
    #     ans = do_autio(js)
    elif scode == 7:
        ans = do_emotion()
    elif scode == 8:
        ans = do_neteasy_music()
    elif scode == 9:
        ans = do_baike(js)
    elif scode == 10:
        ans = do_searchs(js)
    return ans


def do_private(js: dict):
    user_id = int(js['user_id'])
    message = js['message']
    my_time = get_time()
    ans = get_ans(js, -1)
    if ans == None:
        return

    qq_msg = QQ_temp(user_id, MY_QQ_ID, my_time, message, -1)
    qq_ans = QQ_temp(MY_QQ_ID, user_id, my_time, ans, -1)

    with app.app_context():
        db.session.add(qq_msg)
        db.session.add(qq_ans)
        db.session.commit()

    qq_send = {"user_id": user_id, "message": ans}
    requests.post(url=QQ_PRITE_URL, json=qq_send)


def do_group(js: dict):
    message = js['message']
    if str(MY_QQ_ID) not in message:
        return

    message = message.replace(f'[CQ:at,qq={MY_QQ_ID}]', '').strip()
    js['message'] = message
    group_id = int(js['group_id'])
    user_id = int(js['user_id'])
    ans = get_ans(js, group_id)
    my_time = get_time()

    qq_msg = QQ_temp(user_id, MY_QQ_ID, my_time, message, group_id)
    qq_ans = QQ_temp(MY_QQ_ID, user_id, my_time, ans, group_id)

    with app.app_context():
        db.session.add(qq_msg)
        db.session.add(qq_ans)
        db.session.commit()

    qq_send = {"group_id": group_id, "message": ans}
    requests.post(url=QQ_GROUP_URL, json=qq_send)


def do_else(js: dict):
    post_type = js['post_type']
    pass
