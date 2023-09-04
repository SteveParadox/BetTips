
from celery import shared_task
from celery.contrib.abortable import AbortableTask

from Prediction.models import *
from Prediction.process import teams, df_analysis, high_gf_ga



@shared_task(bind=True, base=AbortableTask)
def high_scoring_rate(self):
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
    
    high_scoring_teams, _, _ = high_gf_ga(data)
    for high_gf in high_scoring_teams:
        team = Teams.query.filter_by(name=high_gf).first()
        high_scoring = HighScoring(
                    team = team.name,
                    league = team.league_name,
                    goal_scored = team.gf
                    scoring_rate = team.gf / team.played
        )
        db.session.add(high_scoring)
    db.session.commit()


@shared_task(bind=True, base=AbortableTask)
def high_conceding_rate(self):
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
    
    _, high_conceding_teams, _ = high_gf_ga(data)
    for high_ga in high_conceding_teams:
        team = Teams.query.filter_by(name=high_ga).first()
        high_conceding = HighConceding(
                    team = team.name,
                    league = team.league_name,
                    goal_scored = team.ga
                    scoring_rate = team.ga / team.played
        )
        db.session.add(high_conceding)
    db.session.commit()