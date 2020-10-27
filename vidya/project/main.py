# main.py
# uses https://pypi.org/project/giantbomb-redux/ to return game info
import config
import csv
import random
import requests
import urllib
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, Flask
from flask_login import login_required, current_user
from giantbomb import giantbomb

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
@login_required
def home():
    # Needs giantbomb api key
    gb = giantbomb.Api(config.api_key ,'API test')

    with open('video_game.csv') as f:
        reader = csv.reader(f)
        row = random.choice(list(reader))
    
    game_lookup = row[1]
    
    # returns a list object
    results = gb.search(game_lookup)
    game_data = gb.get_game(results[0])

    

    if game_data.original_release_date is None:
        release = "N/A"
    else:
        release = game_data.original_release_date
    
    if game_data.publishers is None:
        pub = "N/A"
    else:
        pub = game_data.publishers[0]['name']

    if game_data.genres is None:
        genre = "N/A"
    else:
        genre = game_data.genres[0].name

    if game_data.description is None:
        trunc_soup = "N/A"
    else:
        htmltxt = game_data.description
    
        # BeatufiulSoup returns clean text 
        soup = BeautifulSoup(htmltxt, 'lxml').text
    
        # Remove first 8 characters of Description ==> Overview
        c_soup = soup[8:]

        #Truncate the length of descritption
        trunc_soup = (c_soup[:250]) if len(soup) > 1000 else c_soup
    
    
    game = [game_data.name, release, pub,
            game_data.image.medium_url, genre, trunc_soup]
    



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

    
    return render_template('main.html', name=current_user.name, game=game)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
