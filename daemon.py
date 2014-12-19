import SocketServer
import json
import sqlite3
from pymon import app
from flask import g


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


class MyTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True


class MyTCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            data = json.loads(self.request.recv(1024).strip().decode("utf-8"))



        except Exception, e:
            print "Exception wile receiving message: ", e


server = MyTCPServer(('0.0.0.0', 7330), MyTCPServerHandler)
server.serve_forever()