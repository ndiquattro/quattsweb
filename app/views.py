from flask import render_template
from app import app
from mcstatus import MinecraftServer


@app.route('/')
@app.route('/index')
def index():

    return "Under Construction [Man digging gif]"


@app.route('/mcb')
def mcb():

    # Look up server
    server = MinecraftServer.lookup('98.244.54.58:25565')
    ip = '{}:{}'.format(server.host, server.port)

    # Ping the server
    stat = None
    rawinfo = None
    players = None
    try:
        ping = server.ping()
    except:
        playnum = 'None'
    else:
        stat = 1

    if stat == 1:
        # Get query info
        rawinfo = server.query().raw
        players = server.query().players.names

    return render_template('mcb.html',
                           stat=stat,
                           pnum=int(rawinfo['numplayers']),
                           names=players,
                           ver=rawinfo['version'],
                           ip=ip)
