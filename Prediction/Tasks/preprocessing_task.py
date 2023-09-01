from celery import shared_task
from celery.contrib.abortable import AbortableTask
from time import sleep
from Prediction.models import *

from ..url_list import urls
from Prediction.process import teams, df_analysis


@shared_task(bind=True, base=AbortableTask)
def commit_teams(self):
    data = teams()
    for team_data in data: 
        team = Teams(
            name=team_data[0],
            league_name= team_data[1],
            played=team_data[2],
            won=team_data[3],
            drawn=team_data[4],
            lost=team_data[5],
            gf=team_data[6],
            ga=team_data[7],
            gd=team_data[8],
            points=team_data[9],
            Last_5_W= team_data[10],
            Last_5_D= team_data[11],
            Last_5_L= team_data[12],
            team_form=team_data[13],
            win_rate=team_data[14],
            loss_rate=team_data[15],
            draw_rate=team_data[16],
            performance_trend=team_data[17],
            outcome=team_data[18]
        )
        db.session.add(team)
    db.session.commit()


@shared_task(bind=True, base=AbortableTask)
def inform_teams(self):
def inform_teams(self):
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
    
    for_team, against_team, any_win =df_analysis(data)
    if for_team is not None:
        for inform_ in for_team:
            team = Teams.query.filter_by(name=inform_).first()
            inform = InForm(
                        team = team.name,
                        league = team.league_name,
                        win_percent = team.win_rate
            )
            db.session.add(inform)
        db.session.commit()
    print('Data Is Empty')
    


@shared_task(bind=True, base=AbortableTask)
def hello(self):
    print('Hello App')