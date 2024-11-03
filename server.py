from bs4 import BeautifulSoup
from flask import Flask, send_file, send_from_directory, Response
from werkzeug.exceptions import NotFound
from werkzeug.security import safe_join
from threading import Thread
import queue
import logging


# SSE code from https://maxhalford.github.io/blog/flask-sse-no-deps/
def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg

class MessageAnnouncer:
    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]


def run_web_server(announcer: MessageAnnouncer, host: str="localhost", port: int=5000, directory: str="./"):
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app = Flask(__name__)

    @app.route("/---/listen")
    def listener():
        def stream():
            messages = announcer.listen()
            while True:
                msg = messages.get()
                yield msg
        return Response(stream(), mimetype="text/event-stream")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch(path: str):
        if path.endswith(".html"):
            try:
                with open(safe_join(directory, path), "r") as file:
                    return inject_script(file.read())
            except FileNotFoundError:
                raise NotFound
        return send_from_directory(directory, path)

    Thread(target=lambda: app.run(host, port)).start()

def inject_script(html):
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.new_tag("script")
    script_tag.string = """const listener = new EventSource("/---/listen");listener.onmessage = (event) => {window.location.reload()};"""
    soup.find("head").append(script_tag)
    return str(soup)


if __name__ == '__main__':
    announcer = MessageAnnouncer()
    run_web_server(announcer=announcer, host="localhost", port=5000, directory="out/")