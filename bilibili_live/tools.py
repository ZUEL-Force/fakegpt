from private import *
import requests
from random import randint


def to_gpt(msg: str):
    sys_msg = {"role": "system", "content": SYSTEM_MSG}
    user_msg = {"role": "user", "content": msg}
    my_chat = [sys_msg, user_msg]
    to_chat = {"messages": my_chat}
    ans = requests.post(url=GPT_URL, json=to_chat).json()
    if ans['state'] == 0:
        text = ans['msg']['result']
        return text, 0
    return '响应超时，请稍后再试。', 1


def do_repeat(msg: str):
    speaker = SPEAKER[randint(0, len(SPEAKER) - 1)]
    msg = msg.strip()
    # if len(msg) == 0:
    #     return 'E:复读内容过短'
    # elif len(msg) > 100:
    #     return '复读内容过长'

    ans = requests.post(TTS_URL, json={
        'message': msg,
        'speaker': speaker
    }).json()
    if ans['state'] == 0:
        audio_url = AUDIO_REMOTE + ans['msg']['result']
        return audio_url, 0
    else:
        return ans['msg']['result'], 1
