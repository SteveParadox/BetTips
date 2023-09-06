import requests
from bs4 import BeautifulSoup
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import log_loss
import numpy as np
from .url_list import urls


def teams():
    data = []
    data_ = []
    outcome = None
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        h1_tag = soup.find("h1")
        league_name = h1_tag.get_text()
        league_name = league_name.replace("Table & Standings", "").strip()
        table = soup.find("table")
        if table is not None:
            rows = table.find_all("tr")
            for row in rows[1:]:
                columns = row.find_all("td")
                name = row["data-team-name"]
                played = int(row.find("td", {"class": "widget-match-standings__matches-played"}).text.strip())
                won = int(row.find("td", {"class": "widget-match-standings__matches-won"}).text.strip())
                drawn = int(row.find("td", {"class": "widget-match-standings__matches-drawn"}).text.strip())
                lost = int(row.find("td", {"class": "widget-match-standings__matches-lost"}).text.strip())
                gf = int(row.find("td", {"class": "widget-match-standings__goals-for"}).text.strip())
                ga = int(row.find("td", {"class": "widget-match-standings__goals-against"}).text.strip())
                gd = int(row.find("td", {"class": "widget-match-standings__goals-diff"}).text.strip())
                points = int(row.find("td", {"class": "widget-match-standings__pts"}).text.strip())
                dd =row.find("td", {"class": "widget-match-standings__last-five"}).text.strip()
                _data = dd.strip().split('\n')
                row_list = []

                row_list = [row.split() for row in _data][0]
                # Converting the last five results into a win-draw-loss record
                last_five_record = [0, 0, 0]  # Wins, Draws, Losses

                last_five_record[0] = row_list.count("W")
                last_five_record[1] = row_list.count("D")
                last_five_record[2] = row_list.count("L")

                team_form = last_five_record[0] - (last_five_record[1] * last_five_record[2])
                if played > 5:
                    win_rate = won / played
                    loss_rate = lost / played
                    draw_rate = drawn / played
                    performance_trend = (last_five_record[0] - last_five_record[2]) / 5

                    data_.append([name, league_name, played, won, drawn, lost, gf, ga, gd, points,
                                last_five_record[0], last_five_record[1],
                                last_five_record[2], team_form, win_rate, loss_rate, draw_rate, performance_trend])

                    if loss_rate <= 0.45 or win_rate >= 0.65:
                        outcome = 1
                    elif loss_rate >= 0.6 or win_rate <= 0.35:
                        outcome = 0
                    elif draw_rate < 0.35:
                        outcome = 2

                    data.append(data_[-1] + [outcome])

    return data



def df_analysis(data):
    dff = pd.DataFrame(data, columns=["Team", "League", "Played", "Won", "Drawn", "Lost",
                                    "GF", "GA", "GD", "Points", "Last_5_W",
                                    "Last_5_D", "Last_5_L", "Team_Form",
                                    "Win_rate", "Loss_rate", "Draw_rate",
                                    "Performance_trend","Outcome"])

    try:
        df = dff.query('Team_Form >= 2 or Team_Form <= -1')
    except:
        pass

    # Encoding the labels
    le = LabelEncoder()
    le.fit(df["Team"])

    # Splitting the data into training and testing sets
    X = df.drop(columns=["Outcome", "League"])
    y = df["Outcome"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Transforming the labels
    X_train["Team"] = le.transform(X_train["Team"])
    X_test["Team"] = le.transform(X_test["Team"])

    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Evaluating the model on the testing data
    y_pred = rf_model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')    

    try:
        # Getting predictions for all the data
        all_data = pd.concat([X_train, X_test])
        all_predictions = rf_model.predict(all_data)
        all_outcome = pd.concat([y_train, y_test])

        # Getting the team names and outcomes
        team_names = le.inverse_transform(all_data["Team"])
        outcomes =  le.inverse_transform(all_outcome)
        predictions = le.inverse_transform(all_predictions)

        # Creating a dataframe with team names and their predicted outcomes
        team_predictions = pd.DataFrame({"Team": team_names, "Outcome": outcomes, "Prediction": predictions})

        # Printing the teams to be considered as favorites
        for_team = team_predictions[le.transform(team_predictions["Prediction"]) == 1]["Team"].values

        # Printing the teams with poor form
        against_team = team_predictions[le.transform(team_predictions["Prediction"]) == 0]["Team"].values

        # Printing the teams that can potentially win any match
        any_win = team_predictions[le.transform(team_predictions["Prediction"]) == 2]["Team"].values

        return for_team, against_team, any_win

    except Exception as e:
        print(f"Error: {e}")
        return None
# In form team, Teams to bet against




import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
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



def high_gf_ga(data):
    dff = pd.DataFrame(data, columns=["Team", "League", "Played", "Won", "Drawn", "Lost",
                                    "GF", "GA", "GD", "Points", "Last_5_W",
                                    "Last_5_D", "Last_5_L", "Team_Form",
                                    "Win_rate", "Loss_rate", "Draw_rate",
                                    "Performance_trend","Outcome"])
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
    

    return high_scoring_teams, high_conceding_teams, threshold_high_goal_scoring


def predict_both_teams_score(self, compiled, threshold_high_goal_scoring, data):
    dff = pd.DataFrame(data, columns=["Team", "League", "Played", "Won", "Drawn", "Lost",
                                    "GF", "GA", "GD", "Points", "Last_5_W",
                                    "Last_5_D", "Last_5_L", "Team_Form",
                                    "Win_rate", "Loss_rate", "Draw_rate",
                                    "Performance_trend","Outcome"])
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
