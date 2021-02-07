# importing libraries
from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework
import uuid # using random string generator
from ..models import * # importing classes from models.py 
from Site import db, app # importing database and app configuration from folder package
from flask_login import current_user, login_required, login_user, logout_user # using flask login
from werkzeug.security import check_password_hash, generate_password_hash # using flask security
import datetime
# registering blueprint 
edit = Blueprint('edit', __name__)



@edit.route('/')
def home():

    pick = RandomPrediction.query.filter(RandomPrediction.dateUploaded >= (datetime.datetime.now() - datetime.timedelta(days=1))).all()
    prediction = RandomPrediction.query.filter(RandomPrediction.dateUploaded >= (datetime.datetime.now() - datetime.timedelta(days=7))).all()

    return render_template('index.html', pick=pick)


@edit.route('/post', methods=['GET','POST'])
def post():


    return render_template('post.html')

@edit.route('/update', methods=['GET','POST'])
def update():


    return render_template('post.html')



@edit.route('/contact')
def contact():

    return render_template('contact.html')


@edit.route('/in-form-teams', methods=['GET','POST'])
def mostInFormTeams():

    return render_template('informteam.html')



@edit.route('/betting-tips', methods=['GET','POST'])
def bettingTips():

   return render_template('betting-tips.html')

@edit.route('/teams-with-high-scoring-stats', methods=['GET','POST'])
def teamsWithHighGoalStats():


    return render_template('high-scoring-stats.html')

@edit.route('/both-team-score-tips', methods=['GET','POST'])
def bothTeamScoreTips():

    return render_template('both-team-score.html')



@edit.route('/teams-with-high-conceding-rate', methods=['GET','POST'])
def teamsWithHighConcedingRate():

    return render_template('high-conceding.html')


@edit.route('/teams-to-bet-against', methods=['GET','POST'])
def teamsToBetAgainst():

    return render_template('bet-against.html')

@edit.route('/sure-odds', methods=['GET','POST'])
def sureOdds():

    return render_template('sure-odds.html')


@edit.route('/championship-draws', methods=['GET','POST'])
def championshipDraw():

    return render_template('championship-draws.html')