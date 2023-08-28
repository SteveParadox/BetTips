import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from celery import shared_task
from celery.contrib.abortable import AbortableTask
from time import sleep
from Prediction.models import *

start_date = datetime.today() + timedelta(days=1)
end_date = start_date + timedelta(days=2)
delta = timedelta(days=1)
match_fix = []


while start_date <= end_date:
    date_str = start_date.strftime('%d-%B-%Y')
    url = f'https://www.skysports.com/football/fixtures-results/{date_str}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    fixtures = soup.find_all('div', class_='fixres__item')
    for fixture in fixtures:
        league = fixture.find_previous_sibling('h5').text.strip()
        team_1 = fixture.find('span', class_='swap-text__target').text.strip()
        team_2 = fixture.find_all('span', class_='swap-text__target')[1].text.strip()
        time = fixture.find('span', class_='matches__date').text.strip()
        match_fix.append(f'{team_1} vs {team_2}')

    start_date += delta

@shared_task(bind=True, base=AbortableTask)
def get_fixtures(match_fix, self):
    for_team, against_team, any_win = prediction()

    match_fix = np.array(match_fix)
    selection_set = np.array([line.strip() for line in for_team])
    compiled_for = np.array([item for item in match_fix if np.any(np.isin(item.split(' vs '), selection_set))] )

    selection_set_against = np.array([line.strip() for line in against_team])
    compiled_against = np.array([item for item in match_fix if np.any(np.isin(item.split(' vs '), selection_set_against))])

    selection_set_any = np.array([line.strip() for line in any_win])
    compiled_any = np.array([item for item in match_fix if np.any(np.isin(item.split(' vs '), selection_set_any))])
    
    compiled_for = [[s.strip() for s in item.split('vs')] for item in compiled_for]
    compiled_against = [[s.strip() for s in item.split('vs')] for item in compiled_against]
    compiled_any = [[s.strip() for s in item.split('vs')] for item in compiled_any]
    
    return compiled_for, compiled_against, compiled_any



@shared_task(bind=True, base=AbortableTask)
def high_gf_ga(self):
    high_scoring_teams = []
    high_conceding_team = []

    dff['Average_GF_per_Match'] = dff['GF'] / dff['Played']
    dff['Average_GA_per_Match'] = dff['GA'] / dff['Played']
    mean_avg_goal_per_match = dff['Average_GF_per_Match'].mean()
    std_deviation_avg_goal_per_match = dff['Average_GF_per_Match'].std()

    mean_avg_goal_against_per_match = dff['Average_GA_per_Match'].mean()
    std_deviation_avg_goal_against_per_match = dff['Average_GA_per_Match'].std()

    threshold_high_goal_scoring = mean_avg_goal_per_match + std_deviation_avg_goal_per_match
    threshold_high_goal_conceding = mean_avg_goal_against_per_match + std_deviation_avg_goal_against_per_match

    high_scoring_teams = dff[dff['Average_GF_per_Match'] > threshold_high_goal_scoring]['Team'].tolist()
    high_conceding_teams = dff[dff['Average_GA_per_Match'] > threshold_high_goal_conceding]['Team'].tolist()
    
    compiled = compiled_for + compiled_against + compiled_any


    return high_scoring_teams, high_conceding_teams, threshold_high_goal_scoring


def predict_both_teams_score(self, compiled, threshold_high_goal_scoring):
    predictions = []
    for fixture in compiled:
        team_1, team_2 = fixture[0], fixture[1]
        try:
            team_1_gf = dff[dff['Team'] == team_1]['GF'].values[0] +\
             dff[dff['Team'] == team_1]['GA'].values[0]
            team_2_gf = dff[dff['Team'] == team_2]['GF'].values[0] +\
             dff[dff['Team'] == team_2]['GA'].values[0]

            if team_1_gf >= threshold_high_goal_scoring and team_2_gf >= threshold_high_goal_scoring:
                predictions.append(f'{team_1} vs {team_2}: Both Teams to Score')
            else:
                predictions.append(f'{team_1} vs {team_2}: Both Teams Not to Score')

        except IndexError:
           # print(f"Team data not found for {team_1} or {team_2}. Skipping...")
            pass
        
    return predictions
