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


def insert_to_bd(_name, _srv_id, _memory, _disk, _cpu, _processes, _uptime):
    g.db.execute('insert into servers(name, srv_id, memory, disk, cpu, processes, uptime) values(?,?,?,?,?,?,?)', _name,
                 int(_srv_id), _memory, _disk, _cpu, _processes, _uptime)


def update_server(_srv_id, _memory, _disk, _cpu, _processes, _uptime):
    g.db.execute('update  servers set  memory = ?, disk = ?, cpu = ?, processes = ?, uptime = ? where srv_id = ?',
                 _memory, _disk, _cpu, _processes, _uptime, int(_srv_id))


def select_srv_id(_srv_id):
    cur = g.db.execute('select * from servers where srv_id = ?', int(_srv_id))
    if len(cur.ferchall()) == 1:
        return True
    else:
        return False

print select_srv_id(326)


class MyTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True


class MyTCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            data = json.loads(self.request.recv(1024).strip().decode("utf-8"))
            print data['srv_id']
            #print "%s, %s, %s, %s, %s, %s, %s " % data['name'], data['srv_id'], data['memory'], data['disk'], data['cpu'], data['processes'], data['uptime']

            if select_srv_id(data['srv_id']):
                update_server(data['srv_id'], data['memory'], data['disk'], data['cpu'], data['processes'],
                              data['uptime'])
            else:
                insert_to_bd(data['name'], data['srv_id'], data['memory'], data['disk'], data['cpu'], data['processes'],
                             data['uptime'])
        except Exception, e:
            print "Exception wile receiving message: ", e


server = MyTCPServer(('0.0.0.0', 7330), MyTCPServerHandler)
server.serve_forever()