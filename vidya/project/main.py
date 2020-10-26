# main.py

from flask import Blueprint, render_template, Flask
from flask_login import login_required, current_user
import csv
import random
import requests
import rawgpy
import json


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
@login_required
def home():
       
    with open('video_game.csv') as f:
        reader = csv.reader(f)
        row = random.choice(list(reader))

    game = {
        'id': row[0],
        'name': row[1],
        'platform': row[2],
        'release_year': row[3],
        'genre': row[4],
        'publisher': row[5],
        'na_players': row[6],
        'eu_players': row[7],
        'jp_players': row[8],
        'other_players': row[9],
        'global_players': row[10],
        'critic_score': row[11],
        'critic_count': row[12],
        'user_score': row[13],
        'user_count': row[14],
        'developer': row[15],
        'rating': row[16],


    }


    #GET https://api.rawg.io/api/platforms?key=apikey={confiig.api_key}
    #resp = requests.get(https://rawg.io/api/games?search=Warframe)
    
    return render_template('main.html', name=current_user.name, game=game)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)