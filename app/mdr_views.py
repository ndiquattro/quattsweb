from flask import render_template, request
from app import app
import sqlite3 as lite
import pandas as pd
import os

# Database path
if os.uname()[0] == 'Darwin':
    DBPATH = 'scripts/midnight_standings.db'
else:
    DBPATH = 'quattsweb/scripts/midnight_standings.db'


@app.route('/midnightstandings/top')
@app.route('/midnightstandings/')
def mdr_top():

    # Retrieve information
    con = lite.connect(DBPATH)
    with con:
        counts = pd.read_sql_query('SELECT * FROM counts', con)

    # Absolute counts
    winners = counts.sort(['Winner', 'Winper'], ascending=False).head(10).reset_index()
    runners = counts.sort(['Runnerup', 'Runper'], ascending=False).head(10).reset_index()
    losers = counts.sort(['Lastplace', 'Lastper'], ascending=False).head(10).reset_index()

    # Control
    cats = [winners, runners, losers]
    names = ['Most Wins', 'Most Runner-ups', 'Most Losses']

    return render_template('mdr_top.html',
                           names=names,
                           cats=cats,
                           title='@midnight standings - Top 10')


@app.route('/midnightstandings/full')
def mdr_full():

    # Retrieve information
    con = lite.connect(DBPATH)
    with con:
        counts = pd.read_sql_query('SELECT * FROM counts', con)

    # Sort
    scols = ['Winner', 'Runnerup', 'Ties', 'Lastplace']
    ranks = counts.sort(scols, ascending=False).reset_index()

    return render_template('mdr_full.html',
                           ranks=ranks,
                           title='@midnight standings - Full Rankings')


@app.route('/midnightstandings/stats')
def mdr_stats():

    # Get data
    con = lite.connect(DBPATH)
    with con:
        counts = pd.read_sql_query('SELECT * FROM counts', con)

    # Calculate Undefeated streak
    streak = counts[(counts['Runnerup'] == 0) &
                    (counts['Lastplace'] == 0) &
                    (counts['Ties'] == 0)].sort('Winner', ascending=False)

    streak = streak[streak.Winner == max(streak.Winner)].reset_index(drop=True)

    # Most appearances
    apps = counts[counts.Total == max(counts.Total)]

    # Most Ties
    ties = counts[counts.Ties == max(counts.Ties)]

    return render_template('mdr_stats.html',
                           streak=streak,
                           apps=apps,
                           ties=ties)


@app.route('/midnightstandings/profile')
def profile():

    # Get Name
    name = request.args.get('name').replace('_', ' ')

    # Get info about this person
    csql = 'SELECT * FROM counts WHERE Names = "{}"'.format(name)
    ssql = 'SELECT * FROM shows WHERE Winner="{0}" OR Runnerup LIKE "%{0}%" OR Lastplace="{0}"'.format(name)
    con = lite.connect(DBPATH)
    with con:
        counts = pd.read_sql_query(csql, con)
        shows = pd.read_sql_query(ssql, con)

    return render_template("mdr_profile.html",
                           counts=counts.to_dict(orient='records')[0],
                           shows=shows,
                           name=name,
                           title='@midnight standings - {}'.format(name))

@app.route('/midnightstandings/recent')
def recent():

    # Connect to db
    rsql = 'SELECT * FROM shows ORDER BY shownum DESC LIMIT 4'
    con = lite.connect(DBPATH)
    with con:
        rshows = pd.read_sql_query(rsql, con)

    return render_template("mdr_recent.html",
                           shows=rshows,
                           title='@midnight standings - Recent Results')
