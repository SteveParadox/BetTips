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
