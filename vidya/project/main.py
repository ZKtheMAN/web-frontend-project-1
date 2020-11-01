# uses giantbomb API to return game info
# uses BeautifulSoup to parse game description from giantbomb
# flask_login: login requred used to make sure only logged in users can see pages, current_user: contains user currently logged in
# sqlalchemy, Flask-SQLAlchemy: database tookit 
import random, requests, csv,config
from . import db
from .models import UserLikes
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, Flask, url_for, redirect, request, flash
from flask_login import login_required, current_user
from giantbomb import giantbomb
main = Blueprint('main', __name__)
# Shows login/ signup page when user not logged in
@main.route('/')
def index():
    return render_template('index.html')

# Shows main page where user can swipe left or right
# requires POST to handle content posted when swiping right
@main.route('/home', methods = ["GET", "POST"])
@login_required
def home():
    # Needs giantbomb api key
    gb = giantbomb.Api(config.api_key,'API test')
    # Reads a random game from the catalog
    with open('video_game.csv') as f:
        reader = csv.reader(f)
        row = random.choice(list(reader))
    game_lookup = row[1]

    # Giantbomb-Redux API method call
    # returns a list object
    results = gb.search(game_lookup)
    game_data = gb.get_game(results[0])

    #If game_data return was NONE
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
        # Game description returned as html txt
        htmltxt = game_data.description
        # BeatufiulSoup returns clean text 
        soup = BeautifulSoup(htmltxt, 'lxml').text
        # Remove first 8 characters of Description ==> Overview
        c_soup = soup[8:]
        #Truncate the length of descritption
        trunc_soup = (c_soup[:250]) if len(soup) > 1000 else c_soup
    # Game object being passed to main.html   
    game = [game_data.name, release, pub,
            game_data.image.medium_url, genre, trunc_soup, gid]
    # If user clicked the like button, POST sends back data
    if request.method == "POST":
        uId=current_user.id
        # Object return is dictionary
        dict_ret= request.form.to_dict()
        # Iterate through dictinary to retrieve val, holds gameId string
        key,val = next(iter(dict_ret.items()))
        # gameId to integer
        gId=int(val)
        # check if UserLikes Table already contains the entry
        if not UserLikes.query.filter_by(userId=current_user.id, gameId=gId).first():
        # add entry to table  
            uLikes= UserLikes(userId=uId, gameId=gId)
            db.session.add(uLikes)
            db.session.commit()
        # go to home page to get new game suggestion
        redirect(url_for('main.home'))

    return render_template('main.html', name=current_user.name, game=game)

@main.route('/profile')
@login_required
def profile():
    # get logged in user entries
    results = UserLikes.query.filter_by(userId=current_user.id)
    names = []
    gb = giantbomb.Api(config.api_key,'API test')
    count = 0
    for result in results:
        try:
            game = gb.get_game(result.gameId)
            count +=1
        except giantbomb.GiantBombError: #probably a residual ID from the CSV, just skip it
            continue
        names.append(game.name)
    # returns names to profile.html to populate info
    return render_template('profile.html', name=current_user.name,titles=names,count=count)



    