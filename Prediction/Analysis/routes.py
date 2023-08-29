from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework
import uuid 
from ..models import  Teams, InForm, Bts, BettingTips, HighScoring, HighConceding, TeamsSchema
from Prediction import db, app 
import datetime
from Prediction.Tasks.preprocessing_task import commit_teams

# registering blueprint 
analysis = Blueprint('analysis', __name__)

@analysis.route('/api/teams')
def add_teams():
    commit_teams.delay()
    return jsonify({'message': 'done'})

@analysis.route('/api')
def home():
    return jsonify({'message': 'Heheheheh'})

@analysis.route('/api/all_teams')
def teams():
    results = Teams.query.all()
    teams_schema = TeamsSchema(many=True)
    res = teams_schema.dump(results)
    return jsonify(res)
