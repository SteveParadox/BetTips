
from celery import shared_task
from celery.contrib.abortable import AbortableTask

from Prediction.models import *
from Prediction.process import teams, df_analysis, high_gf_ga, match_fix, predict_both_teams_score


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
    high_scoring_teams, _, _ = high_gf_ga(data)
    for high_gf in high_scoring_teams:
        team = Teams.query.filter_by(name=high_gf).first()
        high_scoring = HighScoring(
                    team = team.name,
                    league = team.league_name,
                    goal_scored = team.gf,
                    scoring_rate = float(team.gf) / float(team.played)
        )
        db.session.add(high_scoring)
    db.session.commit()


@shared_task(bind=True, base=AbortableTask)
def high_conceding_rate(self):
    data = get_data()
    _, high_conceding_teams, _ = high_gf_ga(data)
    for high_ga in high_conceding_teams:
        team = Teams.query.filter_by(name=high_ga).first()
        high_conceding = HighConceding(
                    team = team.name,
                    league = team.league_name,
                    goal_conceded = team.ga,
                    conceding_rate = team.ga / team.played
        )
        db.session.add(high_conceding)
    db.session.commit()


@shared_task(bind=True, base=AbortableTask)
def both_teams_score(self):
    data = get_data()
    predictions = predict_both_teams_score(match_fix, data)
    for pred in predictions:
        team = Teams.query.filter_by(name=pred[0]).first()
        bts = Bts(
                    fixture = predictions,
                    league = team.league_name,
                    prediction = ""
        )
        db.session.add(bts)
    db.session.commit()


@shared_task(bind=True, base=AbortableTask)
def anyteamwin(self):
    data = get_data()
    _, _, any_win =df_analysis(data)

    predictions = predict_both_teams_score(match_fix, data, any_win)
    for pred in predictions:
        team = Teams.query.filter_by(name=pred[0]).first()
        h_or_a = H_or_A(
                    fixture = predictions,
                    league = team.league_name,
        )
        db.session.add(h_or_a)
    db.session.commit()

