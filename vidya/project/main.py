# main.py

import csv
import json
import random
import requests
import urllib
from urllib.parse import urlparse
from urllib.parse import urljoin
from requests.utils import requote_uri
from flask import Blueprint, render_template, Flask
from flask_login import login_required, current_user

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
    game_lookup = row[1]
    game_plat = row[2].lower()
    
    old_url = "https://chicken-coop.p.rapidapi.com/games/"+ game_lookup
    new_url=requote_uri(old_url)
    url =  new_url
    plat = game_plat
    querystring = {"platform": plat}

    

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    r_dump = json.dumps(data)

    for r in 
    #GET https://api.rawg.io/api/platforms?key=apikey={confiig.api_key}
    #resp = requests.get(https://rawg.io/api/games?search=Warframe)
    
    return render_template('main.html', name=current_user.name, game=g_name)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)