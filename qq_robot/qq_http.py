import json
from flask import request

from my_tools import right
from my_basic import app
from my_class import init_db
from private import MY_APP_PORT
from qq_receive import do_group, do_else, do_private
from qq_send import sched, check_receive, check_send


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


if __name__ == '__main__':
    # init_db()
    sched.add_job(id='check_receive',
                  func=check_receive,
                  trigger='interval',
                  seconds=1,
                  max_instances=4)
    sched.add_job(id='check_send',
                  func=check_send,
                  trigger='interval',
                  seconds=1,
                  max_instances=4)

    sched.start()
    app.run(debug=True, host="0.0.0.0", port=MY_APP_PORT)
    # app.run(host="0.0.0.0", port=MY_APP_PORT)
