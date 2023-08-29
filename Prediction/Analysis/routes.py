from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework
import uuid 
from ..models import  Teams, InForm, Bts, BettingTips, HighScoring, HighConceding
from Prediction import db, app 
import datetime
from Prediction.Tasks.preprocessing_task import commit_teams

# registering blueprint 
analysis = Blueprint('analysis', __name__)

@analysis.route('/api/teams')
def add_teams():
    commit_teams.delay()
    return jsonify({'message': 'done'})
