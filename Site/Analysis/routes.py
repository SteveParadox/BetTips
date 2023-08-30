from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework
import uuid 
from ..models import * 
from Site import db, app 
import datetime
from Site.editor.form import NotificationForm


# registering blueprint 
analysis = Blueprint('analysis', __name__)

def handle_prediction_view(template_name):
    form = NotificationForm()
    
    if form.validate_on_submit():
        notify = Notification()
        notify.name = form.name.data
        notify.email = form.email.data
        db.session.add(notify)
        db.session.commit()
        
        return redirect(url_for('edit.home'))
    
    return render_template(template_name, form=form)

@analysis.route('/in-form-teams', methods=['GET', 'POST'])
def mostInFormTeams():
    in_form = InForm.query.order_by(InForm.date_uploaded.desc()).all()[:25]

    return render_template( 'informteam.html', in_form=in_form)

@analysis.route('/betting-tips', methods=['GET', 'POST'])
def bettingTips():
    betting_tips = BettingTips.query.order_by(BettingTips.date_uploaded.desc()).all()[:25]

    return render_template('betting-tips.html', betting_tips=betting_tips)

@analysis.route('/teams-with-high-scoring-stats', methods=['GET', 'POST'])
def teamsWithHighGoalStats():
    high_scoring = HighScoring.query.order_by(HighScoring.date_uploaded.desc()).all()[:25]

    return render_template('high-scoring-stats.html', high_scoring=high_scoring)

@analysis.route('/both-team-score-tips', methods=['GET', 'POST'])
def bothTeamScoreTips():
    bts_tip = Bts.query.order_by(Bts.date_uploaded.desc()).all()[:25]

    return render_template( 'both-team-score.html', bts_tip=bts_tip)

@analysis.route('/teams-with-high-conceding-rate', methods=['GET', 'POST'])
def teamsWithHighConcedingRate():
    high_conceding = HighConceding.query.order_by(HighConceding.date_uploaded.desc()).all()[:25]

    return render_template('high-conceding.html', high_conceding=high_conceding)

@analysis.route('/teams-to-bet-against', methods=['GET', 'POST'])
def teamsToBetAgainst():
    betagainst = BetAgainst.query.order_by(BetAgainst.date_uploaded.desc()).all()[:25]

    return render_template( 'bet-against.html', betagainst=betagainst)

@analysis.route('/teams/statistics', methods=['GET', 'POST'])
def team_statistics():
    betagainst = BetAgainst.query.order_by(BetAgainst.date_uploaded.desc()).all()[:25]

    return render_template( 'statistics.html', betagainst=betagainst)

@analysis.route('/sure-odds', methods=['GET', 'POST'])
def sureOdds():
    return handle_prediction_view(SureOdds, 'sure-odds.html')

@analysis.route('/championship-draws', methods=['GET', 'POST'])
def championshipDraw():
    return handle_prediction_view(Championship, 'championship-draws.html')


@analysis.route('/search', methods=['GET', 'POST'])
def searchfile():
    return render_template('statistics.html')


@analysis.route('/searche', methods=['POST'])
def search():
    data = request.form.get('text')
    results = Teams.query.filter(Teams.name.ilike(f'%{data}%')).all()
    teams_schema = TeamsSchema(many=True)
    res = teams_schema.dump(results)
    return jsonify(res)



@analysis.route('/<string:name>', methods=['POST'])
def team_detail(name):
    results = Teams.query.filter_by(name=name).first()
    teams_schema = TeamsSchema(many=True)
    res = teams_schema.dump(results)
    return jsonify(res)
