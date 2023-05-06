import warnings
import queue
from bilibili_api import live, sync
from private import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tools import *
import threading
import subprocess

warnings.filterwarnings('ignore')

QuestionQueue = queue.Queue(10)  #定义 弹幕队列、名称队列、回复队列、播放队列
UserNameQueue = queue.Queue(10)
AnswerQueue = queue.Queue()
PlayQueue = queue.Queue()

room = live.LiveDanmaku(LIVE_ID)  # 连接弹幕服务器

sched = AsyncIOScheduler(timezone="Asia/Shanghai")

is_gpt_ready = True  # 定义gpt是否回复完成标志，请联系OS课中的进程互斥理解
is_tts_ready = True  # 定义语音是否生成完成标志
is_play_ready = True  # 定义是否播放完成标志


@room.on('DANMU_MSG')
async def on_danmu(event):
    '''
    处理弹幕信息
    '''
    global QuestionQueue, UserNameQueue
    content = event['data']['info'][1]  #弹幕内容
    user_name = event['data']['info'][2][1]  #用户昵称
    print(rf"{user_name}:{content}")  #打印弹幕
    if not QuestionQueue.full():
        UserNameQueue.put(user_name)
        QuestionQueue.put(content)
        print('\033[32mSystem>>\033[0m已将该条弹幕添加入问题队列')
    else:
        print('\033[32mSystem>>\033[0m队列已满，该条弹幕被丢弃')


def gpt_response():
    '''
    从问题队列中选择一条，生成回复并存入回复队列。
    '''
    global QuestionQueue, AnswerQueue, UserNameQueue, is_gpt_ready
    prompt = QuestionQueue.get()
    user_name = UserNameQueue.get()
    response, state = to_gpt(prompt)
    if state != 0:
        is_gpt_ready = True
        return
    answer = f'回复{user_name}：{response}'
    AnswerQueue.put(answer)
    question_count = QuestionQueue.qsize()
    print(f"\033[31m[chatGPT]\033[0m{answer}")  # 打印AI回复信息
    print(
        f'\033[32mSystem>>\033[0m[{user_name}]的回复已存入队列，当前剩余问题数:{question_count}'
    )
    is_gpt_ready = True  #该轮gpt已回复完毕


def check_answer():
    '''
    如果AI没有在生成回复且队列中还有问题 则创建一个生成回复的线程
    '''
    global is_gpt_ready, QuestionQueue, AnswerQueue
    if not QuestionQueue.empty() and is_gpt_ready:
        is_gpt_ready = False
        answer_thread = threading.Thread(target=gpt_response())
        answer_thread.start()


def tts_generate():
    '''
    从回复队列中提取一条，通过tts生成对应语音
    '''
    global is_tts_ready, AnswerQueue, PlayQueue
    response = AnswerQueue.get()
    audio_url, state = do_repeat(response)
    if state != 0:  #如果音频合成失败则直接抛弃，不回复了
        return
    PlayQueue.put(audio_url)
    begin_name = response.find('回复')
    end_name = response.find("：")
    name = response[begin_name + 2:end_name]
    print(f'\033[32mSystem>>\033[0m对[{name}]的回复已成功转换为语音并缓存为output{audio_url}')
    is_tts_ready = True


def check_tts():
    '''
    如果语音已播放完成且队列中还有回复 则创建一个生成并播放语音的线程
    '''
    global is_tts_ready
    if not AnswerQueue.empty() and is_tts_ready:
        is_tts_ready = False
        tts_thread = threading.Thread(target=tts_generate())
        tts_thread.start()


def play_read():
    '''
    播放playqueue中的内容直至播放完毕
    '''
    global PlayQueue, is_play_ready
    while not PlayQueue.empty():
        temp = PlayQueue.get()
        # playqueue_count = PlayQueue.qsize()
        # print(
        #     f'\033[32mSystem>>\033[0m开始播放output{temp}，当前待播语音数：{playqueue_count}'
        # )
        with open('audio.wav', 'wb') as f:
            f.write(requests.get(temp).content)
        subprocess.run(f'mpv.exe -vo null audio.wav 1>nul', shell=True)
        subprocess.run(f'del audio.wav', shell=True)
        # subprocess.run(f'mpv.exe -vo null {temp} 1>nul', shell=True)
    is_play_ready = True


def check_play():
    '''
    若已经播放完毕且播放列表中有数据，则创建一个新的音频线程
    '''
    global is_play_ready, PlayQueue
    if not PlayQueue.empty() and is_play_ready:
        is_play_ready = False
        tts_thread = threading.Thread(target=play_read())
        tts_thread.start()


if __name__ == '__main__':
    sched.add_job(check_answer,
                  'interval',
                  seconds=1,
                  id=f'answer',
                  max_instances=4)
    sched.add_job(check_tts,
                  'interval',
                  seconds=1,
                  id=f'mytts',
                  max_instances=4)
    sched.add_job(check_play,
                  'interval',
                  seconds=1,
                  id=f'mpv',
                  max_instances=4)
    sched.start()
    sync(room.connect())
