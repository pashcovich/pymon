import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

basedir = os.path.abspath(os.path.dirname(__file__))
# configuration
DATABASE = os.path.join(basedir, 'pymon.db')
DEBUG = True
SECRET_KEY = 'PyMon super secret key'
USERNAME = 'admin'
PASSWORD = 'admin'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('PYMON_SETTINGS', silent=True)


# database functions
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('database.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

'''
_______*
______/|\
_____/|0|\
____/|||0|\
____/||0||\
___/|0|||||\
__/|0|||||0|\
___/|0||0||\
__/|||0|||0|\
_/|0/||0||\||\
_____|...|
_____|...|___
HAPPY_NEW_YEAR
'''


@app.route('/select/<_srv_id>')
def sel(_srv_id):
    cur = g.db.execute('select name, srv_id, memory, disk, cpu, processes, uptime  from servers where srv_id = ?', (_srv_id,))

    server = [dict(id=_srv_id, name=row[0], srv_id=row[1], memory=row[2], disk=row[3], cpu=row[4], processes=row[5],
                   uptime=row[6]) for row in cur.fetchall()]
    return "%s " % server

# views functions
@app.route('/')
def index():
    return render_template("index.html", title="Dashboard")


@app.route('/settings')
def settings():
    cur = g.db.execute('select id, name from server_groups')
    grps = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
    return render_template("settings.html", title="Settings", groups=grps)


@app.route('/settings/groups')
def stng_groups():
    cur = g.db.execute('select id, name from server_groups')
    grps = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
    return render_template("settings_groups.html", title="Settings", groups=grps)

@app.route('/settings/stats')
def stng_stats():
    cur = g.db.execute('select id, name from server_groups')
    grps = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
    return render_template("settings_stats.html", title="Settings", groups=grps)


@app.route('/profile')
def profile():
    return render_template("profile.html", title="Profile")


@app.route('/servers')
def servers():
    cur = g.db.execute('select id, name, srv_id, uptime, memory, disk, cpu, processes  from servers')
    srvs = [dict(id=row[0], name=row[1], srv_id=row[2], uptime=row[3], memory=row[4], disk=row[5], cpu=row[6],
                 processes=row[7]) for row in cur.fetchall()]
    return render_template("servers.html", servers=srvs, title="Servers")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['login'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/detail/<serverid>')
def server_detail(serverid):
    cur = g.db.execute('select name, srv_id, memory, disk, cpu, processes, uptime  from servers where id = ?', (serverid,))
    server = [dict(id=serverid, name=row[0], srv_id=row[1], memory=row[2], disk=row[3], cpu=row[4], processes=row[5],
                   uptime=row[6]) for row in cur.fetchall()]
    return render_template('server_info.html', server=server, title="Details")


if __name__ == '__main__':
    app.run(debug=True)