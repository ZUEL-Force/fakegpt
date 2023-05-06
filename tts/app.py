import json

from flask import request
from my_tools import *
from mybasic import app
from private import PTH_DICT
from moeGoe import vits_tts


@app.route('/text_to_speak/', methods=['GET', 'POST'])
def text_to_speak():
    data = request.get_data()
    js = json.loads(data)
    message = js['message']
    speaker = js['speaker']
    if speaker not in PTH_DICT.keys():
        return wrong({'result': f"'{speaker}' not in speakers."})
    wav, state = vits_tts(message, speaker)
    if state == 1:
        return wrong({'result': f"{wav}"})
    return right({'result': f'/static/audio/{wav}'})


@app.route('/get_speakers/', methods=['GET', 'POST'])
def get_speakers():
    speakers = PTH_DICT
    return right({'result': speakers})


if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0", port=11114)
    app.run(host="0.0.0.0", port=11115, debug=True)
