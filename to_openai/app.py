import json

from api_openai import *
from flask import Response, request, stream_with_context
from mybasic import app
from myTools import *


@app.route('/talk/', methods=['POST'])
def talk():
    data = request.get_data()
    js = json.loads(data)
    que = js['messages']
    if que == None:
        return wrong({'result': "Parameter error"})

    result, state = chatgpt(que)

    if state == 0:
        return right({'result': result})
    return wrong({'result': result})


@app.route('/stream_talk/', methods=['POST'])
def stream_talk():
    data = request.get_data()
    js = json.loads(data)
    que = js['messages']
    if que == None:
        return wrong({'result': "Parameter error"})

    return Response(stream_with_context(get_stream(que)),
                    content_type='application/json')


@app.route('/create_img/', methods=['POST'])
def create_img():
    data = request.get_data()
    js = json.loads(data)
    que = js['messages']
    if que == None:
        return wrong({'result': "Parameter error"})

    result, state = dalle(que)

    if state == 0:
        return right({'result': result})
    return wrong({'result': result})


@app.route('/speak_to_text/', methods=['POST'])
def speak_to_text():
    return wrong({'result': '接口暂未开通'})


if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0", port=11112)
    app.run(host="0.0.0.0", port=11113)
