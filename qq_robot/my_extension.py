import re
from io import BytesIO
from pathlib import Path
from random import randint
import requests
from PIL import Image

from my_tools import get_salt, to_baike, get_weather, get_que_key
from private import *
from my_tables import get_pre_msgs
from my_class import TEMP_MSG

speaker = 'kokomi'


def do_talk(message: str, temp_msg: TEMP_MSG):
    sys_msg = {"role": "system", "content": SYSTEM_MSG}
    my_chat = [sys_msg]
    pre_chat = get_pre_msgs(temp_msg)
    my_chat += pre_chat
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


def do_help():
    return "胖熊还没写help，以后再说"


def do_ban(message: str, gid: str):
    ban_list = re.findall(r"禁言\[CQ:at,qq=\d+\]", message)

    if len(ban_list) != 1 or str(MY_QQ_ID) in ban_list[0]:
        return "格式错误，应为'@机器人 禁言@禁言对象'"

    ban_id = re.findall(r"\d+", ban_list[0])[0]
    ban_send = {
        "group_id": gid,
        "user_id": ban_id,
        "duration": 60,
    }
    requests.post(url=QQ_BAN_URL, json=ban_send)
    return "好的，已禁言[CQ:at,qq=%s]" % ban_id


def do_pic(message: str):
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


def do_alter_audio(message: str):
    global speaker

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


def do_repeat(message: str):
    global speaker

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
        # audio_file = Path(audio_url)
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
        return '网易云失败，请稍后重试。'
    except:
        return '网易云失败，请稍后重试。'


def do_baike(msg: str):
    msg = msg.replace('百度', '')
    msg = msg.replace('百科', '')
    msg = msg.strip()
    if len(msg) > 10:
        return '搜索内容过长。'
    res, state = to_baike(msg)
    return res


def do_searchs(msg: str):
    sys_msg = {"role": "system", "content": SYSTEM_MSG}
    my_chat = [sys_msg]

    keys = get_que_key(msg)
    for key in keys:
        print('key=', key)
        text, state = to_baike(key)
        if state == 0:
            user_msg = {"role": "user", "content": text}
            my_chat.append(user_msg)
    my_chat.append({"role": "user", "content": msg})
    to_chat = {"messages": my_chat}

    # for it in to_chat['messages']:
    #     print(it)

    ans = requests.post(url=GPT_URL, json=to_chat).json()
    if ans['state'] == 0:
        text = str(ans['msg']['result'])
        return text
    return '后台服务超时，请稍后再试。'


def do_weather(msg: str):
    msg = msg.replace('天气', '')
    msg = msg.strip()

    result, state = get_weather(msg)
    print(f'msg={msg},result={result}')
    return result


def do_clear_sing(msg: str):
    msg = msg.replace('清唱', '')
    msg = msg.strip()

    if len(msg) == 0:
        return '请指定歌名'

    if speaker not in SINGER_DICT.keys():
        return '当前音色不支持唱歌'

    if msg not in SONG_DICT.keys():
        return '当前歌曲暂未收录'

    clear_path = Path.joinpath(Path(SINGER_DICT[speaker]), 'clear')
    clear_path = Path.joinpath(clear_path, f'{SONG_DICT[msg]}.wav')
    if clear_path.is_file():
        return '[CQ:record,file=%s]' % clear_path.as_uri()
    return '当前歌曲暂未收录'


def do_sing(msg: str):
    msg = msg.replace('点歌', '')
    msg = msg.replace('唱歌', '')
    msg = msg.strip()

    if len(msg) == 0:
        return '请指定歌名'

    if speaker not in SINGER_DICT.keys():
        return '当前音色不支持唱歌'

    if msg not in SONG_DICT.keys():
        return '当前歌曲暂未收录'

    sing_path = Path.joinpath(Path(SINGER_DICT[speaker]), 'sing')
    sing_path = Path.joinpath(sing_path, f'{SONG_DICT[msg]}.wav')
    if sing_path.is_file():
        return '[CQ:record,file=%s]' % sing_path.as_uri()
    return '当前歌曲暂未收录'
