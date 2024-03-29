
from celery import shared_task
from celery.contrib.abortable import AbortableTask

from Prediction.models import *
from Prediction.process import teams, df_analysis, high_gf_ga, match_fix, predict_both_teams_score, predict_home_or_away
from random import sample
import math 

def get_data():
    teams = Teams.query.all()
    data = [[
        team.name,
        team.league_name,
        team.played,
        team.won,
        team.drawn,
        team.lost,
        team.gf,
        team.ga,
        team.gd,
        team.points,
        team.Last_5_W,
        team.Last_5_D,
        team.Last_5_L,
        team.team_form,
        team.win_rate,
        team.loss_rate,
        team.draw_rate,
        team.performance_trend,
        team.outcome
    ] for team in teams]

    return data

@shared_task(bind=True, base=AbortableTask)
def high_scoring_rate(self):
    data = get_data()
    high_scoring_teams, _, _ = high_gf_ga(match_fix, data)
    for high_gf in high_scoring_teams:
        team = Teams.query.filter_by(name=high_gf).first()
        high_scoring = HighScoring(
                    team = team.name,
                    league = team.league_name,
                    goal_scored = team.gf,
                    scoring_rate = round((float(team.gf) / float(team.played)), 2)
        )
        db.session.add(high_scoring)
    db.session.commit()


@shared_task(bind=True, base=AbortableTask)
def high_conceding_rate(self):
    data = get_data()
    _, high_conceding_teams, _ = high_gf_ga(match_fix, data)
    for high_ga in high_conceding_teams:
        team = Teams.query.filter_by(name=high_ga).first()
        if team is not None:
            high_conceding = HighConceding(
                        team = team.name,
                        league = team.league_name,
                        goal_conceded = team.ga,
                        conceding_rate = round((team.ga / team.played), 2)
            )
            db.session.add(high_conceding)
    db.session.commit()


@shared_task(bind=True, base=AbortableTask)
def both_teams_score(self):
    data = get_data()
    bts_list = Bts.query.order_by(Bts.week.desc()).all()
    predictions = predict_both_teams_score(match_fix, data)
    for pred in predictions:
        pred_ = pred.split(' vs ')
        team = Teams.query.filter_by(name=pred_[0]).first()
        if team is not None:
            if bts_list:
                bts = bts_list[0]
                bts_ = Bts(
                    fixture=str(pred),
                    league=team.league_name,
                    prediction=0.0,
                    week=bts.week + 1
                )
                bts_list.pop(0)
            else:
                bts_ = Bts(
                    fixture=str(pred),
                    league=team.league_name
                )
            
            db.session.add(bts_)

    db.session.commit()



@shared_task(bind=True, base=AbortableTask)
def anyteamwin(self):
    h_a_list = H_or_A.query.order_by(H_or_A.week.desc()).all()
    data = get_data()
    _, _, any_win = df_analysis(data)

    predictions = predict_home_or_away(match_fix, data, any_win)
    
    for pred in predictions:
        pred_ = pred.split(' vs ')
        team = Teams.query.filter_by(name=pred_[0]).first()
        if team is not None:

            if h_a_list:
                h_a = h_a_list[0]  # Get the first element
                h_or_a = H_or_A(
                    fixture=str(pred),
                    league=team.league_name,
                    week=h_a.week + 1
                )
                h_a_list.pop(0) 
            else:
                h_or_a = H_or_A(
                    fixture=str(pred),
                    league=team.league_name
                )
            
            db.session.add(h_or_a)

    db.session.commit()


def get_random():
    random_rows = []

    random_rows.extend(InForm.query.order_by(db.func.random()).limit(2).all())
    random_rows.extend(HighScoring.query.order_by(db.func.random()).limit(2).all())
    random_rows.extend(HighConceding.query.order_by(db.func.random()).limit(2).all())
    random_rows.extend(H_or_A.query.order_by(db.func.random()).limit(2).all())
    random_rows.extend(Bts.query.order_by(db.func.random()).limit(2).all())

    return random_rows

@shared_task(bind=True, base=AbortableTask)
def bettingpick(self):
    random_rows = get_random()
    bpicks = BettingTips.query.order_by(BettingTips.week.desc()).all()
    bettips = BettingTips()
    for row in random_rows:
        if isinstance(row, InForm):
            bettips = BettingTips(
                team=row.team,
                competition=row.league,
                prediction="To Win",
                confidence=0.0
            )
        elif isinstance(row, HighScoring):
            bettips = BettingTips(
                team=row.team,
                competition=row.league,
                prediction=f"To score Over {round(row.scoring_rate, 1)} goals",
                confidence=0.0
            )
        elif isinstance(row, HighConceding):
            bettips = BettingTips(
                team=row.team,
                competition=row.league,
                prediction=f"To Concede Over {round(row.conceding_rate, 1)} goals",
                confidence=0.0
            )
        elif isinstance(row, H_or_A):
            bettips = BettingTips(
                team=row.fixture,
                competition=row.league,
                prediction=row.prediction,
                confidence=0.0
            )
        elif isinstance(row, Bts):
            bettips = BettingTips(
                team=row.fixture,
                competition=row.league,
                prediction=row.prediction,
                confidence=0.0
            )
        if bpicks:
            bpicks = bpicks[0]
            bettips.week = bpicks.week + 1
        db.session.add(bettips)
    db.session.commit()
