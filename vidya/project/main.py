# main.py
# uses https://pypi.org/project/giantbomb-redux/ to return game info
import config
import csv
from giantbomb import giantbomb
import random
import requests
import urllib
from flask import Blueprint, render_template, Flask
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
@login_required
def home():
    # Needs giantbomb api key
    gb = giantbomb.Api(config.api_key,'API test')

    with open('video_game.csv') as f:
        reader = csv.reader(f)
        row = random.choice(list(reader))
    
    game_lookup = row[1]
    game = []
    # returns a list object
    results = gb.search(game_lookup)
    game_data = gb.get_game(results[0])
    game.append(game_data.name)
    game.append(game_data.original_release_date)
    if game_data.publishers is not None:
        game.append(game_data.publishers[0]['name'])
    else:
        game.append("")
    game.append(game_data.image.medium_url)
    
    if game_data.genres is not None:
        if not game_data.genres[0].name:
            game.append("")
        else:
            game.append(game_data.genres[0].name)
    else:
        game.append("")
    
    return render_template('main.html', name=current_user.name, game=game, gLookup=game_lookup)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)