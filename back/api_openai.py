import os

import openai

import private
from config import AUDIO_FOLDER, MODEL

openai.api_key = private.API_KEY


def chatgpt(que: list):
    response = openai.ChatCompletion.create(model=MODEL[0], messages=que)
    text = response['choices'][0]['message']['content']
    reason = response['choices'][0]['finish_reason']
    cost = response['usage']['total_tokens']
    text = str(text).strip()
    return [text, reason, cost]


#TODO:语音转文字
def whisper(file: str):
    audio_file = open(os.path.join(AUDIO_FOLDER, file), 'rb')
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]


#TODO:文字转图片
def dalle():
    pass


# if __name__ == '__main__':
#     path, file = 'static/audio', 'test.mp3'
#     transcript = whisper(path, file)
#     print(transcript)
