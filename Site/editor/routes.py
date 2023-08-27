# importing libraries
from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework
import uuid # using random string generator
from ..models import * # importing classes from models.py 
from Site import db, app # importing database and app configuration from folder package
import datetime
import os
import time
from Site.models import InForm, BetAgainst, BettingTips, Bts, HighScoring, HighConceding, Teams
from .utils import load_league, read_from_txt
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


@edit.route('/0', methods=['GET','POST'])
def _():
    data = load_league("data.txt")
    for item in data:
        teams = Teams()
        teams.name =  item['name']     
        teams.played = item['played']
        teams.won = item['won']
        teams.drawn = item['drawn']
        teams.lost = item['lost']
        teams.gf = item['gf']
        teams.ga = item['ga']
        teams.gd = item['gd']
        teams.points = item['points']
        teams.team_form = item['team_form']
        teams.win_rate = item['win_rate']
        teams.loss_rate = item['loss_rate']
        teams.draw_rate = item['draw_rate']
        teams.performance_trend = item['performance_trend']
        teams.db.session.add(teams)
    db.session.commit()

    return 'done'
    

@edit.route('/1', methods=['GET','POST'])
def a():
    data = load_league('for_team.txt')
    for item in data:
        in_form = InForm()
        in_form.content = item['team']
        in_form.league = item['league']
        in_form.country = item['country']
        db.session.add(in_form)
    db.session.commit()

    return 'done'


@edit.route('/2', methods=['GET','POST'])
def b():
    data = load_league('any_win.txt')
    for item in data:
        in_form = BettingTips()
        in_form.content = item['team']
        in_form.league = item['league']
        in_form.country = item['country']
        db.session.add(in_form)
    db.session.commit()

    return 'done'



@edit.route('/3', methods=['GET','POST'])
def c():
    data = load_league('high_scoring_teams.txt')
    for item in data:
        in_form = HighScoring()
        in_form.content = item['team']
        in_form.league = item['league']
        in_form.country = item['country']
        db.session.add(in_form)
    db.session.commit()

    return 'done'

@edit.route('/4', methods=['GET','POST'])
def d():
    data = load_league('high_conceding_teams.txt')
    for item in data:
        in_form = HighConceding()
        in_form.content = item['team']
        in_form.league = item['league']
        in_form.country = item['country']
        db.session.add(in_form)
    db.session.commit()

    return 'done'


@edit.route('/5', methods=['GET','POST'])
def e():
    data = load_league('bts_predictions.txt')
    for item in data:
        in_form = Bts()
        in_form.content = item['team']
        in_form.league = item['league']
        in_form.country = item['country']
        db.session.add(in_form)
    db.session.commit()

    return 'done'


@edit.route('/6', methods=['GET','POST'])
def f():
    data = load_league('against_team.txt')
    for item in data:  
        bet_against = BetAgainst()

        bet_against.content = item['team']
        bet_against.league = item['league']
        bet_against.country = item['country']
        db.session.add(bet_against)
    db.session.commit()

    return 'done'

@edit.route('/7', methods=['GET','POST'])
def g():
    form= sureOddsForm()
    if form.validate_on_submit():
        sureodd = SureOdds()
        sureodd.content= form.content.data
        sureodd.country = form.country.data
        sureodd.league = form.league.data
        db.session.add(sureodd)
        db.session.commit()
        return redirect(url_for("edit.g"))


    return render_template('post.html', form=form, legend='Sure odds')

@edit.route('/8', methods=['GET','POST'])
def h():
    form= championshipDrawForm()
    if form.validate_on_submit():
        champ = Championship()
        champ.content= form.content.data
        champ.country = form.country.data
        champ.league = form.league.data
        db.session.add(champ)
        db.session.commit()
        return redirect(url_for("edit.h"))

    return render_template('post.html', form=form, legend='Championship draws')

@edit.route('/9', methods=['GET','POST'])
def i():
    form= RandomPickForm()
    if form.validate_on_submit():
        rand= RandomPrediction()
        rand.content= form.content.data
        rand.country = form.country.data
        rand.league = form.league.data
        db.session.add(rand)
        db.session.commit()
        return redirect(url_for("edit.i"))

    return render_template('post.html', form=form, legend='Random picks')

@edit.route('/contact')
def contact():

    return render_template('contact.html')

