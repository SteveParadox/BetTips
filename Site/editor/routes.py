# importing libraries
from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework
import uuid # using random string generator
from ..models import * # importing classes from models.py 
from Site import db, app # importing database and app configuration from folder package
from flask_login import current_user, login_required, login_user, logout_user # using flask login
from werkzeug.security import check_password_hash, generate_password_hash # using flask security
import datetime
from Site.editor.form import *
import os
import time
from Site.models import InForm
from .utils import load_league

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
    

@edit.route('/1', methods=['GET','POST'])
def a():
   
    prediction = InForm(content=team, country=country, league=league)
    
    db.session.add(prediction)

    db.session.commit()

    return 'DONE'


@edit.route('/2', methods=['GET','POST'])
def b():
    form= Tips()
    if form.validate_on_submit():
        bettips= BettingTips()
        bettips.content= form.content.data
        bettips.country = form.country.data
        bettips.league = form.league.data
        db.session.add(bettips)
        db.session.commit()
        return redirect(url_for("edit.b"))
    return render_template('post.html', form=form, legend='Betting Tips')



@edit.route('/3', methods=['GET','POST'])
def c():
    form = HighGoalStats()
    if form.validate_on_submit():
        highscoring= HighScoring()
        highscoring.content= form.content.data
        highscoring.country = form.country.data
        highscoring.league = form.league.data
        db.session.add(highscoring)
        db.session.commit()
        return redirect(url_for("edit.c"))
    return render_template('post.html', form=form, legend='High scoring stats')


@edit.route('/4', methods=['GET','POST'])
def d():
    form= Bothteamsscore()
    if form.validate_on_submit():
        bts= Bts()
        bts.content = form.content.data
        bts.country = form.country.data
        bts.league = form.league.data
        db.session.add(bts)
        db.session.commit()
        return redirect(url_for("edit.d"))
    return render_template('post.html', form=form, legend='Both teams to score')



@edit.route('/5', methods=['GET','POST'])
def e():
    form = HighConcedingRate()
    if form.validate_on_submit():
        highconcede = HighConceding()
        highconcede.content = form.content.data
        highconcede.country = form.country.data
        highconcede.league = form.league.data
        db.session.add(highconcede)
        db.session.commit()
        return redirect(url_for("edit.e"))
    return render_template('post.html', form=form, legend='High concedeing rate')




@edit.route('/6', methods=['GET','POST'])
def f():
    data = load_league('against_team.txt')
    bet_against = BetAgainst()
    for items in data:
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

