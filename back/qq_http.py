import json

from flask import request

from mybasic import app
from qq_server import *


@app.route('/myqq/', methods=['GET', 'POST'])
def myqq():
    data = request.get_data()
    js = json.loads(data)
    if js['post_type'] == 'message':
        m_type = js['message_type']
        if m_type == 'private':
            do_private(js)
        else:
            do_group(js)
    else:
        do_else(js)
    return right("ok")


# TODO: 机器人发语音、发图片

if __name__ == '__main__':
    # init_db()
    app.run(debug=True, host="0.0.0.0", port=11112)
    # app.run(host="0.0.0.0", port=11112)
