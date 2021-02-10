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

import json
import uuid
import os

from flask import Blueprint, render_template, request, jsonify

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import DataRequired



class InFormTeam(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')



class Tips(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class HighGoalStats(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class Bothteamsscore(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class HighConcedingRate(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class BetAgainst(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')



class sureOddsForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')



class championshipDrawForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class RandomPickForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class NotificationForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    submit = SubmitField('Subscribe')

@edit.route('/', methods=['GET','POST'])
def home():

    pick = RandomPrediction.query.all()
    prediction = RandomPrediction.query.filter(RandomPrediction.dateUploaded >= (datetime.datetime.now() - datetime.timedelta(days=7))).all()
    form = NotificationForm()
    if form.validate_on_submit():
        notify = Notification()
        notify.name = form.name.data
        notify.email = form.email.data
        db.session.add(notify)
        db.session.commit()

        return redirect(url_for('edit.home'))
    return render_template('index.html', pick=pick, form=form)


@edit.route('/1', methods=['GET','POST'])
def a():
    form = InFormTeam()
    if form.validate_on_submit():
        inform= InForm()
        inform.content = form.content.data
        inform.country = form.country.data
        inform.league = form.league.data
        db.session.add(inform)
        db.session.commit()
        return redirect(url_for("edit.a"))
    
    return render_template('post.html', form=form, legend='In Form Teams')


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
    
    form= BetAgainst()
    if form.validate_on_submit():
        betagainst= BetAgainst()
        betagainst.content = form.content.data
        betagainst.country = form.country.data
        betagainst.league = form.league.data
        db.session.add(betagainst)
        db.session.commit()
        return redirect(url_for("edit.f"))
    return render_template('post.html', form=form, legend='Teams to bet against')


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


@edit.route('/in-form-teams', methods=['GET','POST'])
def mostInFormTeams():
    inform = InForm.query.all()
    form = NotificationForm()
    if form.validate_on_submit():
        notify = Notification()
        notify.name = form.name.data
        notify.email = form.email.data
        db.session.add(notify)
        db.session.commit()
        
        return redirect(url_for('edit.home'))
    return render_template('informteam.html', inform=inform, form = form)



@edit.route('/betting-tips', methods=['GET','POST'])
def bettingTips():
    bet=BettingTips.query.all()
    form = NotificationForm()
    if form.validate_on_submit():
        notify = Notification()
        notify.name = form.name.data
        notify.email = form.email.data
        db.session.add(notify)
        db.session.commit()
        
        return redirect(url_for('edit.home'))
    return render_template('betting-tips.html',  bet=bet, form= form)

@edit.route('/teams-with-high-scoring-stats', methods=['GET','POST'])
def teamsWithHighGoalStats():
    highscore= HighScoring.query.all()
    form = NotificationForm()
    if form.validate_on_submit():
        notify = Notification()
        notify.name = form.name.data
        notify.email = form.email.data
        db.session.add(notify)
        db.session.commit()
        
        return redirect(url_for('edit.home'))
    return render_template('high-scoring-stats.html',  highscore=highscore,form = form)

@edit.route('/both-team-score-tips', methods=['GET','POST'])
def bothTeamScoreTips():
    bts = Bts.query.all()
    form = NotificationForm()
    if form.validate_on_submit():
        notify = Notification()
        notify.name = form.name.data
        notify.email = form.email.data
        db.session.add(notify)
        db.session.commit()
        
        return redirect(url_for('edit.home'))
    return render_template('both-team-score.html',  bts=bts, form=form)



@edit.route('/teams-with-high-conceding-rate', methods=['GET','POST'])
def teamsWithHighConcedingRate():
    highconcede =HighConceding.query.all()
    form = NotificationForm()
    if form.validate_on_submit():
        notify = Notification()
        notify.name = form.name.data
        notify.email = form.email.data
        db.session.add(notify)
        db.session.commit()
        
        return redirect(url_for('edit.home'))
    return render_template('high-conceding.html', highconcede=highconcede, form=form)


@edit.route('/teams-to-bet-against', methods=['GET','POST'])
def teamsToBetAgainst():
    betagainst = BetAgainst.query.all()
    form = NotificationForm()
    if form.validate_on_submit():
        notify = Notification()
        notify.name = form.name.data
        notify.email = form.email.data
        db.session.add(notify)
        db.session.commit()
        
        return redirect(url_for('edit.home'))
    return render_template('bet-against.html', betagainst=betagainst, form=form)

@edit.route('/sure-odds', methods=['GET','POST'])
def sureOdds():
    sureodds= SureOdds.query.all()
    form = NotificationForm()
    if form.validate_on_submit():
        notify = Notification()
        notify.name = form.name.data
        notify.email = form.email.data
        db.session.add(notify)
        db.session.commit()
        
        return redirect(url_for('edit.home'))
    return render_template('sure-odds.html', sureodds=sureodds, form=form)


@edit.route('/championship-draws', methods=['GET','POST'])
def championshipDraw():
    championship= Championship.query.all()
    form = NotificationForm()
    if form.validate_on_submit():
        notify = Notification()
        notify.name = form.name.data
        notify.email = form.email.data
        db.session.add(notify)
        db.session.commit()
        
        return redirect(url_for('edit.home'))
    return render_template('championship-draws.html', championship=championship, form=form)



