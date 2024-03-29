# importing libraries
from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework
import uuid # using random string generator
from ..models import * # importing classes from models.py 
from Site import db, app, io # importing database and app configuration from folder package
import os
from datetime import datetime, timedelta
import time
from Site.models import InForm, BetAgainst, BettingTips, Bts, HighScoring, HighConceding, Teams
from .form import RandomPickForm
import requests
from flask_socketio import emit

from dotenv import load_dotenv

load_dotenv()
edit = Blueprint('edit', __name__)



@edit.route('/', methods=['GET','POST'])
def home():
    seven_days_ago = datetime.now() - timedelta(days=7)
    pick = RandomPrediction.query.all()
    prediction = RandomPrediction.query.filter(RandomPrediction.date_uploaded >= seven_days_ago).all()
    form = RandomPickForm()
    if form.validate_on_submit():
        notify = RandomPrediction()
        notify.content = form.content.data
        notify.country = form.country.data
        notify.league = form.league.data
        db.session.add(notify)

        db.session.commit()

        return redirect(url_for('edit.home'))
    return render_template('index.html', pick=pick, form=form)



@edit.route('/contact')
def contact():

    return render_template('contact.html')

@edit.route('/create_tables')
def create_tables():
    with app.app_context():
        db.drop_all()
        db.create_all()
    return 'Database tables created successfully'

@edit.route('/home/away/previous')
def last_pred():
    data = H_or_A.query.filter_by(week=week).all()
    bts_data = Bts.query.filter_by(week=week).all()
    bpicks_data = BettingTips.query.filter_by(week=week).all()


    return render_template('previous.html', data=data, bts_data=bts_data, bpicks_data=bpicks_data)



def get_date_strings():
    today_date = datetime.now().date() + timedelta(days=1)
    one_day_from_today = today_date + timedelta(days=2)
    today_date_str = today_date.strftime('%Y-%m-%d')
    one_day_from_today_str = one_day_from_today.strftime('%Y-%m-%d')
    return today_date_str, one_day_from_today_str

@edit.route('/fixture')
@edit.route('/fixture/<date_type>')
def fixture(date_type=None):
    today_date_str, one_day_from_today_str = get_date_strings()

    if date_type == 'tomorrow':
        two_days_from_today = datetime.strptime(one_day_from_today_str, '%Y-%m-%d') + timedelta(days=1)
        two_days_from_today_str = two_days_from_today.strftime('%Y-%m-%d')

        api_url = f"https://apiv3.apifootball.com/?action=get_events&from={one_day_from_today_str}&to={two_days_from_today_str}&APIkey={os.environ.get('Api_Key')}"
        odds_url = f"https://apiv3.apifootball.com/?action=get_odds&from=2023-09-12&to=2023-09-13&APIkey={os.environ.get('Api_Key')}"
    else:
        api_url = f"https://apiv3.apifootball.com/?action=get_events&from={today_date_str}&to={one_day_from_today_str}&APIkey={os.environ.get('Api_Key')}"
        odds_url = f"https://apiv3.apifootball.com/?action=get_odds&from=2023-09-11&to=2023-09-12&APIkey={os.environ.get('Api_Key')}"

    response = requests.get(api_url)
    response_odds = requests.get(odds_url)

    if response.status_code == 200 and response_odds.status_code == 200:
        data = response.json()
        extracted_data = []
        for match_data in data:
            data = {
                "country_name": match_data["country_name"],
                "league_name": match_data["league_name"],
                "league_year": match_data["league_year"],
                "match_date": match_data["match_date"],
                "match_time": match_data["match_time"],
                "match_hometeam_name": match_data["match_hometeam_name"],
                "match_awayteam_name": match_data["match_awayteam_name"],
                "match_stadium": match_data["match_stadium"],
                "match_round": match_data["match_round"],
                "stage_name": match_data["stage_name"]
            }
            extracted_data.append(data)
        return render_template('fixture.html', extracted_data=extracted_data)
    else:
        return "Error: Unable to fetch data from the API", response.status_code


@io.on('connect')
def handle_connect():
    APIkey = os.environ.get('Api_Key')
    socket_url = f'wss://wss.apifootball.com/livescore?Widgetkey={APIkey}&timezone=+01:00'
    
    def on_message(message):
        emit('data', message)  

    socket = None

    try:
        socket = io.AsyncClient()
        socket.connect(socket_url)

        @socket.on('message')
        def handle_message(data):
            on_message(data)

        socket.wait()
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        if socket:
            socket.disconnect()