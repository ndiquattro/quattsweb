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

    # Ping the server
    try:
        ping = server.ping()
    except:
        stat = 'Offline'
        playnum = 'None'
    else:
        stat = 'Online'

    if stat == 'Online':
        # Get players info
        playnum = server.status().players.online
        players = server.query().players.names

    return render_template('mcb.html',
                           stat=stat,
                           pnum=playnum,
                           names=players)
