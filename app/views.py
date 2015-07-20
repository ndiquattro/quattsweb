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
        stat = 'Down'
        playnum = 'No'
    else:
        stat = 'Up'

    if stat == 'Up':
        # Get players info
        playnum = server.status().players.online

    return render_template('mcb.html',
                           stat=stat,
                           pnum=playnum)
