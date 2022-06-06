from flask import Flask, request
from event import create_event
from plugins import archpkg, bing, eatwhat, ecdict, echo, hefeng, help, nasa, qqgroup, translate
import logging
import threading


app = Flask(__name__)
# logging.getLogger('werkzeug').disabled = True


@app.route('/', methods=['POST'])
def _():
    threading.Thread(target=create_event, args=(request.get_json(),), daemon=True).start()
    return ''


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=8801)