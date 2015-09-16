from flask import render_template, request
from . import midnightstandings
import sqlite3 as lite
import pandas as pd

# Database path
DBPATH = 'scripts/midnight_standings.db'


@midnightstandings.route('/')
def top():

    # Retrieve information
    con = lite.connect(DBPATH)
    with con:
        counts = pd.read_sql_query('SELECT * FROM counts', con)

    # Absolute counts
    winners = counts.sort(['Winner', 'Winper'],
                          ascending=False).head(10).reset_index()
    runners = counts.sort(['Runnerup', 'Runper'],
                          ascending=False).head(10).reset_index()
    losers = counts.sort(['Lastplace', 'Lastper'],
                         ascending=False).head(10).reset_index()

    # Control
    cats = [winners, runners, losers]
    names = ['Most Wins', 'Most Runner-ups', 'Most Losses']

    return render_template('top.html',
                           names=names,
                           cats=cats,
                           title='@midnight standings - Top 10')


@midnightstandings.route('/full')
def full():

    # Retrieve information
    con = lite.connect(DBPATH)
    with con:
        counts = pd.read_sql_query('SELECT * FROM counts', con)

    # Sort
    scols = ['Winner', 'Runnerup', 'Ties', 'Lastplace']
    ranks = counts.sort(scols, ascending=False).reset_index()

    return render_template('full.html',
                           ranks=ranks,
                           title='@midnight standings - Full Rankings')


@midnightstandings.route('/stats')
def stats():

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

    # Means
    mns = counts.mean(axis=0).round(2)
    sds = counts.std(axis=0).round(2)

    return render_template('stats.html',
                           streak=streak,
                           apps=apps,
                           ties=ties,
                           means=mns,
                           stds=sds,
                           title='@midnight standings - Statistics')


@midnightstandings.route('/profile/<name>')
def profile(name):

    # Get Name
    name = name.replace('_', ' ')

    # Get info about this person
    csql = 'SELECT * FROM counts WHERE Names = "{}"'.format(name)
    ssql = 'SELECT * FROM shows WHERE Winner="{0}" OR Runnerup LIKE "%{0}%" OR Lastplace="{0}"'.format(name)
    con = lite.connect(DBPATH)
    with con:
        counts = pd.read_sql_query(csql, con)
        shows = pd.read_sql_query(ssql, con)

    return render_template("profile.html",
                           counts=counts.to_dict(orient='records')[0],
                           shows=shows,
                           name=name,
                           title='@midnight standings - {}'.format(name))


@midnightstandings.route('/recent')
def recent():

    # Connect to db
    rsql = 'SELECT * FROM shows ORDER BY shownum DESC LIMIT 4'
    con = lite.connect(DBPATH)
    with con:
        rshows = pd.read_sql_query(rsql, con)

    return render_template("recent.html",
                           shows=rshows,
                           title='@midnight standings - Recent Results')


@midnightstandings.route('/about')
def about():
    return render_template("about.html",
                           title='@midnight standings - About')
