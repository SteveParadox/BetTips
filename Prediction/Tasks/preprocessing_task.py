from celery import shared_task
from celery.contrib.abortable import AbortableTask
from time import sleep
from Prediction.models import *

from ..url_list import urls
from Prediction.process import teams


@shared_task(bind=True, base=AbortableTask)
def commit_teams(self):
    data = teams()
    for team_data in data:  # Assuming 'data' contains the formatted data
        team = Teams(
            name=team_data[0],
            played=team_data[1],
            won=team_data[2],
            drawn=team_data[3],
            lost=team_data[4],
            gf=team_data[5],
            ga=team_data[6],
            gd=team_data[7],
            points=team_data[8],
            team_form=team_data[9],
            win_rate=team_data[10],
            loss_rate=team_data[11],
            draw_rate=team_data[12],
            performance_trend=team_data[13]
        )
        db.session.add(team)
    db.session.commit()


@shared_task(bind=True, base=AbortableTask)
def commit_seperate(self):
    pass

