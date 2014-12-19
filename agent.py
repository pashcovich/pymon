#!/usr/bin/env python
import subprocess
import socket
import json


# config
HOST = "127.0.0.1"
PORT = 7330
SERVERID = 777


def srv_name():
    n = subprocess.Popen("hostname -s", shell=True, stdout=subprocess.PIPE)
    out = n.stdout.read()
    result = out.split()
    return result[0]

def diskusage():
    d = subprocess.Popen("df -h", shell=True, stdout=subprocess.PIPE)
    out = d.stdout.read()
    result = out.split()
    return "%s | %s | %s " % (result[8], result[9], result[10])


def meminfo():
    m = subprocess.Popen("/usr/bin/free -m", shell=True, stdout=subprocess.PIPE)
    out = m.stdout.read()
    result = out.split()
    return "%s | %s | %s" % (result[7], result[8], result[9])


def uptime():
    u = subprocess.Popen("/usr/bin/w", shell=True, stdout=subprocess.PIPE)
    out = u.stdout.read()
    result = out.split()
    return "%s" % result[2]


def la():
    l = subprocess.Popen("/usr/bin/w", shell=True, stdout=subprocess.PIPE)
    out = l.stdout.read()
    result = out.split()
    return "%s | %s | %s" % (result[9], result[10], result[11])


def processes():
    p = subprocess.Popen("/bin/ps -ef | wc -l", shell=True, stdout=subprocess.PIPE)
    out = p.stdout.read()
    result = out.split()
    return int(result[0])-2


l=[("name", srv_name()), ("srv_id", SERVERID), ("memory", meminfo()), ("uptime", uptime()), ("la", la()), ("processes", processes())]

srv_info = dict(list)


srv_info_test = {
    'name': 'Dummy-text-01',
    'srv_id': 326,
    'memory': '1024 | 467 | 557',
    'uptime': '8 days',
    'disk': '20 | 13.4 | 6 .6',
    'la': '0.01 | 0.02 | 0.01'
}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 13373))
s.send(json.dumps(srv_info_test).encode("utf-8"))
s.close()



