#!/home/nickof4/.virtualenvs/quatts/bin/python2.7
# coding=utf-8
# Pulls @midnight results from wikipedia and saves them.
import wikipedia
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3 as lite
import os
import datetime


# Returns results table from wiki page
def dfmaker(pagetitle):

    # Get page HTML and find tables
    wikipage = wikipedia.page(title=pagetitle)
    alltables = BeautifulSoup(wikipage.html(), 'html.parser').find_all('table')

    # Keep tables that have show results
    rtabs = [pd.read_html(str(t), header=0, encoding='utf-8')[0]
             for t in alltables if t.th.text == ' No.\n']
    yeares = pd.concat(rtabs)

    # Clean up dataframe
    newnames = {'Original air date[3]': 'airdate',
                'Original air date': 'airdate',
                'Runner-up': 'Runnerup',
                'Last place': 'Lastplace',
                'No.': 'shownum'}
    yeares.rename(columns=newnames,
                  inplace=True)

    qrem = ['Winner', 'Runnerup', 'Lastplace']
    yeares[qrem] = yeares[qrem].replace(regex='["]', value='')
    yeares.airdate = yeares.airdate.str[:-13]

    results = yeares[pd.notnull(yeares['Winner'])]  # removes not results rows

    return results


# Cleans and incorporates ties
def tiecleaner(sdf):
    # Save a copy of ties and remove from original data frame
    ties = sdf[sdf.index.str.contains('tie')].index.tolist()
    sdf = sdf[stats.index.str.contains('tie') == False]

    # Clean tie strings
    ties = sum([val.replace(' (tie)', '').replace(', ', ' and ').split(' and ')
                for val in ties], [])

    # Count number of ties
    tiecount = pd.value_counts(ties)
    newnames = {0: 'Ties', 'index': 'Names'}
    tiecount = tiecount.reset_index().rename(columns=newnames)

    # Merge ties with original data frame
    df = pd.merge(sdf, tiecount, left_index=True, right_on='Names', how='left')
    df.fillna(0, inplace=True)
    df = df[['Names', 'Winner', 'Runnerup', 'Lastplace', 'Ties']]

    return df


# Grab data from all wiki pages
pages = ["List of @midnight episodes (2013–14)",
         "List of @midnight episodes (2015)"]

bigdf = pd.concat([dfmaker(pages[0]), dfmaker(pages[1])], ignore_index=True)

# Count wins, etc.
stats = bigdf[['Winner', 'Runnerup', 'Lastplace']].apply(pd.value_counts)
stats.fillna(0, inplace=True)

# Account for ties
finaldf = tiecleaner(stats)
finaldf = finaldf[finaldf.Names != 'None']

# Calculate totals etc.
finaldf['Total'] = finaldf.sum(1)
finaldf['Winper'] = (finaldf['Winner'] / finaldf['Total']) * 100
finaldf['Runper'] = (finaldf['Runnerup'] / finaldf['Total']) * 100
finaldf['Lastper'] = (finaldf['Lastplace'] / finaldf['Total']) * 100
finaldf['Tieper'] = (finaldf['Ties'] / finaldf['Total']) * 100

# Save Results
csql = {'Names': 'TEXT', 'Winner': 'INT', 'Runnerup': 'INT',
        'Lastplace': 'INT', 'Ties': 'INT', 'Total': 'INT', 'Winper': 'FLOAT',
        'Runper': 'FLOAT', 'Lastper': 'FLOAT', 'Tieper': 'FLOAT'}

ssql = {'shownum': 'INT'}

con = lite.connect('midnight_standings.db')
with con:
    bigdf.to_sql('shows', con, index=False, if_exists='replace', dtype=ssql)
    finaldf.to_sql('counts', con, index=False, if_exists='replace', dtype=csql)

# Log results
with open(str(os.getcwd()) + '/log.txt', 'a') as f:
    f.write(str(datetime.datetime.now()) + ",success\n")
