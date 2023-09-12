from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework
import uuid 
from ..models import * 
from Site import db, app 
import datetime
from Site.editor.form import NotificationForm
import os
from dotenv import load_dotenv

load_dotenv()

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
    in_form = InForm.query.order_by(InForm.win_percent.desc()).all()[:25]

    return render_template( 'informteam.html', in_form=in_form)

@analysis.route('/betting-tips', methods=['GET', 'POST'])
def bettingTips():
    betting_tips = BettingTips.query.order_by(BettingTips.date_uploaded.desc()).all()[:25]

    return render_template('betting-tips.html', betting_tips=betting_tips)

@analysis.route('/teams-with-high-scoring-stats', methods=['GET', 'POST'])
def teamsWithHighGoalStats():
    high_scoring = HighScoring.query.order_by(HighScoring.scoring_rate.desc()).all()[:25]

    return render_template('high-scoring-stats.html', high_scoring=high_scoring)

@analysis.route('/both-team-score-tips', methods=['GET', 'POST'])
def bothTeamScoreTips():
    bts_tip = Bts.query.order_by(Bts.prediction.desc()).all()[:25]

    return render_template( 'both-team-score.html', bts_tip=bts_tip)

@analysis.route('/teams-with-high-conceding-rate', methods=['GET', 'POST'])
def teamsWithHighConcedingRate():
    high_conceding = HighConceding.query.order_by(HighConceding.conceding_rate.desc()).all()[:25]

    return render_template('high-conceding.html', high_conceding=high_conceding)

@analysis.route('/teams-to-bet-against', methods=['GET', 'POST'])
def teamsToBetAgainst():
    betagainst = BetAgainst.query.order_by(BetAgainst.date_uploaded.desc()).all()[:25]

    return render_template( 'bet-against.html', betagainst=betagainst)

@analysis.route('/teams/statistics', methods=['GET', 'POST'])
def team_statistics():

    return render_template( 'statistics.html')

@analysis.route('/Home/Away', methods=['GET', 'POST'])
def home_or_away():
    anywin = H_or_A.query.order_by(H_or_A.date_uploaded.desc()).all()[:25]

    return render_template( 'any_win.html', anywin=anywin)

@analysis.route('/draws/prediction', methods=['GET', 'POST'])
def championshipDraw():
    return render_template( 'championship-draws.html')


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



@analysis.route('/<string:name>', methods=['GET'])
def team_detail(name):
    team = Teams.query.filter_by(name=name).first()
    team_key = Teamkey.query.filter_by(name=team.name).first()
    if team_key:
        url = f"https://apiv3.apifootball.com/?action=get_H2H&firstTeamId={team_key.key}&secondTeamId={151}&APIkey={os.environ.get('Api_Key')}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            extend = []
            for i in data["firstTeam_lastResults"]:
                data_json = {
                    league_name = i["league_name"],
                    match_date = i["match_date"],
                    hometeam = i["match_hometeam_name"],
                    awayteam = i["match_awayteam_name"],
                    hometeam_score = i["match_hometeam_score"],
                    awayteam_score = i["match_awayteam_score"],
                    hometeam_halftime_score = i["match_hometeam_halftime_score"],
                    awayteam_halftime_score = i["match_awayteam_halftime_score"]
                }
                extend.append(data_json)

            return render_template('team.html',team=team, extend=extend)

@analysis.route('/livescore')
def live():
    return render_template('livescore.html')  

