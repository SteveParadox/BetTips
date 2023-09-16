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
from .url_list import draw_urls as urls
from tqdm import tqdm


def draw_teams():
    data = []
    data_ = []
    outcome = None
    for url in tqdm(urls, desc="Extracting Data"):
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
    dff['Total_Goals'] = dff['GF'] + dff['GA']
    dff['Is_Draw'] = dff['Outcome'] == 'Draw'
    dff['Under_2.5'] = dff['Total_Goals'] < (2.5 * dff['Played'] )
    dff['Recent_Form'] = dff['Last_5_W'] * 3 + dff['Last_5_D']

    return dff

