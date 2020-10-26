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

    headers = {
    'x-rapidapi-host': "chicken-coop.p.rapidapi.com",
    'x-rapidapi-key': "b590a8cafamshdc9be6b93bde56bp18a072jsn109b333e1243"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    d_dump = json.dumps(data)

    g_name = data['result'][5]
    g_date = data['result'][1]
    g_desc = data['result'][2]
    g_genre = data['result'][3][0]
    g_img = data['result'][4]
    g_dev = data['result'][6]
    g_rate = data['result'][8]

 
  

    #GET https://api.rawg.io/api/platforms?key=apikey={confiig.api_key}
    #resp = requests.get(https://rawg.io/api/games?search=Warframe)
    
    return render_template('main.html', name=current_user.name, game=g_name, gLookup=game_lookup, gPlat=game_plat)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)