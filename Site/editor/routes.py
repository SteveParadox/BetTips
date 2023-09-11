# importing libraries
from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework
import uuid # using random string generator
from ..models import * # importing classes from models.py 
from Site import db, app # importing database and app configuration from folder package
import datetime
import os
import time
from Site.models import InForm, BetAgainst, BettingTips, Bts, HighScoring, HighConceding, Teams
from .form import RandomPickForm
import requests

from dotenv import load_dotenv

load_dotenv()
edit = Blueprint('edit', __name__)



@edit.route('/', methods=['GET','POST'])
def home():
    seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
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

@edit.route('/fixture')
def fixture():
    api_url = f"https://apiv3.apifootball.com/?action=get_events&from=2023-09-11&to=2023-09-12&APIkey={os.environ.get('Api_Key')}"
    odds_url=f"https://apiv3.apifootball.com/?action=get_odds&from=2023-09-11&to=2023-09-12&APIkey={os.environ.get('Api_Key')}"

    response = requests.get(api_url)
    response_odds = requests.get(odds_url)


    if response.status_code == 200 and response_odds.status_code == 200:
        data = response.json()
        data_odd = response_odds.json()
        extracted_data = []
        for match_data, odd_data in zip(data, data_odd):
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
                "stage_name": match_data["stage_name"],
                "home_odd": odd_data["odd_1"],
                "draw_odd": odd_data['odd_x'],
                "away_data": odd_data['odd_2']
            }
            extracted_data.append(data)
        return render_template('fixture.html', extracted_data=extracted_data)
    else:
        return "Error: Unable to fetch data from the API", response.status_code

