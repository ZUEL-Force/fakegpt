import openai

import private
from config import MODEL

openai.api_key = private.API_KEY


def ask(que: list):
    response = openai.ChatCompletion.create(model=MODEL[0], messages=que)
    text = response['choices'][0]['message']['content']
    reason = response['choices'][0]['finish_reason']
    cost = response['usage']['total_tokens']
    text = str(text).strip()
    return [text, reason, cost]
