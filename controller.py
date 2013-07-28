from collections import defaultdict
import datetime
from os.path import join, split
import StringIO

from flask import Flask, render_template, redirect, url_for, request, jsonify, Response, flash, send_file
from flask.templating import TemplateNotFound

# Need to clean these up a bit.
import pymongo
import mongo

from settings import SOURCES, STAT_TABLES, SINGLE_SOURCES

soccer_db = mongo.soccer_db

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')



# Issues to work on.
# - show problem rows
# - searchable
# - filters
# - pages


    
@app.route("/")
def index():
    return redirect(url_for('dashboard'))


@app.route("/dashboard")
def dashboard():
    """
    A dashboard for showing the status of all available data.
    """

    def process_scraper(scraper):
        table_names = ['%s_%s' % (scraper, table) for table in STAT_TABLES]
        return [(table_name, soccer_db[table_name].count()) for table_name in table_names]



    # Main is named a little differently. Should probably change this.
    data = [('main', [(table_name, soccer_db[table_name].count()) for table_name in STAT_TABLES]),]
    for e in SOURCES:
        t = (e, process_scraper(e))
        data.append(t)

    small_data = [(coll_name, soccer_db[coll_name].count()) for coll_name in SINGLE_SOURCES]

    ctx = {
        'data': data,
        'small_data': small_data,
        'stat_tables': STAT_TABLES
        }

    return render_template("dashboard.html", **ctx)    



@app.route('/d')
def data():
    """
    Gives back a listing of the elements in the collection.
    Uses the first item to determine which fields to show.
    """
    collection_name = request.args['c']
    collection = soccer_db[collection_name]

    if collection.count():
        keys = sorted(collection.find()[0].keys())
        keys.remove("_id")

        # No good to see.
        if 'url' in keys:
            keys.remove('url')
    else:
        keys = []

    ctx = {
        'keys': keys,
        'data':  collection.find()
        }

    return render_template("data.html", **ctx)




@app.route('/dashboard/<competition>')
def competition_dashboard(competition):
    # Is this still used?

    seasons = [str(e) for e in range(1996, 2011)]

    def get_year_list(coll, seasons):
        season_count = defaultdict(int)
        for item in coll.find({'competition': competition}):
            season = item['season']
            season_count[season] += 1
        return [(season, season_count.get(season, 0)) for season in seasons]
            
            
    game_seasons = get_year_list(soccer_db.games, seasons)
    goal_seasons = get_year_list(soccer_db.goals, seasons)
    stat_seasons = get_year_list(soccer_db.gstats, seasons)
    lineup_seasons = get_year_list(soccer_db.lineups, seasons)
    standing_seasons = get_year_list(soccer_db.standings, seasons)

    ctx = {
        'game_seasons': game_seasons,
        'goal_seasons': goal_seasons,
        'stat_seasons': stat_seasons,
        'lineup_seasons': lineup_seasons,
        'standing_seasons': standing_seasons,
        'seasons': seasons,
        'competition': competition,
        }

    
    return render_template("mls_dashboard.html", **ctx)



if __name__ == "__main__":
    app.run(port=29111)
