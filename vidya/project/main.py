# main.py
# uses https://pypi.org/project/giantbomb-redux/ to return game info
import config
import csv
import random
from random import seed, randint
import requests
import urllib
from . import db
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, Flask, url_for, redirect, request, flash
from flask_login import login_required, current_user
from giantbomb import giantbomb

def function(g):
    return "HELLO"

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/home', methods = ["GET", "POST"])
@login_required
def home():
    # Needs giantbomb api key
    gb = giantbomb.Api(config.api_key,'API test')

    with open('video_game.csv') as f:
        reader = csv.reader(f)
        row = random.choice(list(reader))
    
    game_lookup = row[1]
    
    # returns a list object
    results = gb.search(game_lookup)
    
    game_data = gb.get_game(results[0])

    #if game_data is None:
        

    if game_data.id is None:
        gid = "N/A"
    else: 
        gid = game_data.id
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
            game_data.image.medium_url, genre, trunc_soup, gid]
  
    if request.method == "POST":
        
        uId=current_user.id
        dict_ret= request.form.to_dict()
        # val used to hold game id
        key,val = next(iter(dict_ret.items()))
        gId=int(val)

        uLikes= UserLikes(userId=uId, gameId=gId)
        db.session.add(uLikes)
        db.session.commit()
        redirect(url_for('main.home'))


    return render_template('main.html', name=current_user.name, game=game)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

from .models import UserLikes

@main.route("/likes")
@login_required
def likes():
    results = UserLikes.query.filter_by(userId=current_user.id)
    names = []
    gb = giantbomb.Api(config.api_key,'API test')

    for result in results:
        try:
            game = gb.get_game(result.gameId)
        except giantbomb.GiantBombError: #probably a residual ID from the CSV, just skip it
            continue
        names.append(game.name)

    return render_template('likes.html', titles=names)