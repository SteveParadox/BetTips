from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework
import uuid 
from ..models import  Teams, InForm, Bts, BettingTips, HighScoring, HighConceding, TeamsSchema, AnyteamSchema, TeamkeySchema
from Prediction import db, app 
import datetime
from Prediction.Tasks.preprocessing_task import *
from Prediction.Tasks.postprocessing_tasks import *
from tqdm import tqdm


# registering blueprint 
analysis = Blueprint('analysis', __name__)

@analysis.route('/api/teams')
def add_teams():
    commit_teams.delay()
    return jsonify({'message': 'done'})

@analysis.route('/api')
def home():
    f=[]
    for i in tqdm(range(1,3), desc="Loading... "):
        api_url = f"https://apiv3.apifootball.com/?action=get_teams&league_id={i}&APIkey={os.environ.get('Api_Key')}"
        response = requests.get(api_url)
        f.append(response.json())
    return jsonify({'message': f})

@analysis.route('/api/all_teams')
def teams():
    results = Teams.query.all()
    teams_schema = TeamsSchema(many=True)
    res = teams_schema.dump(results)
    return jsonify(res)

@analysis.route('/api/h_or_a')
def amyteams():
    results = H_or_A.query.all()
    teams_schema = AnyteamSchema(many=True)
    res = teams_schema.dump(results)
    return jsonify(res)

@analysis.route('/api/inform/teams')
def add_inform_teams():
    inform_teams.delay()
    return jsonify({'message': 'done'})

@analysis.route('/api/highgf/teams')
def add_highgf_teams():
    high_scoring_rate.delay()
    return jsonify({'message': 'done'})

@analysis.route('/api/highga/teams')
def add_highga_teams():
    high_conceding_rate.delay()
    return jsonify({'message': 'done'})

@analysis.route('/api/anyteam/teams')
def add_anyteam():
    anyteamwin.delay()
    return jsonify({'message': 'done'})

@analysis.route('/api/bts/teams')
def add_btsteam():
    both_teams_score.delay()
    return jsonify({'message': 'done'})

@analysis.route('/api/bet/picks')
def bet_picks():
    bettingpick.delay()
    return jsonify({'message': 'done'})

@analysis.route('/api/hello')
def home_hello():
    hello.delay()
    return jsonify({'message': 'done'})

@analysis.route('/api/xxx')
def db_create():
    db_refresh.delay()
    return jsonify({'message': 'done'})

@analysis.route('/api/team/key')
def get_team_key():
    team_id.delay()
    return jsonify({'message': 'done'})

@analysis.route('/api/team_key')
def team_key():
    results = Teamkey.query.all()
    teams_schema = TeamkeySchema(many=True)
    res = teams_schema.dump(results)
    return jsonify(res)