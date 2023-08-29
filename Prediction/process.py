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

                    data_.append([name, played, won, drawn, lost, gf, ga, gd, points,
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


def df_analysis():
    data = teams()
    dff = pd.DataFrame(data, columns=["Team", "Played", "Won", "Drawn", "Lost",
                                    "GF", "GA", "GD", "Points", "Last_5_W",
                                    "Last_5_D", "Last_5_L", "Team_Form",
                                    "Win_rate", "Loss_rate", "Draw_rate",
                                    "Performance_trend","Outcome"])
    print(len(dff))


    # In[47]:


    try:
        df = dff.query('Team_Form >= 2 or Team_Form <= -1')
    except:
        pass

    # Encoding the labels
    le = LabelEncoder()
    le.fit(df["Team"])

    # Splitting the data into training and testing sets
    X = df.drop(columns=["Outcome"])
    y = df["Outcome"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Transforming the labels
    X_train["Team"] = le.transform(X_train["Team"])
    X_test["Team"] = le.transform(X_test["Team"])


    print(len(df))


    # In[48]:


    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Evaluating the model on the testing data
    y_pred = rf_model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-score: {f1}")
    return X_test, X_train, y_test, y_train


# In[49]:


def prediction():
    X_test, X_train, y_test, y_train = df_analysis()
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


# In[50]:


for_team, against_team, any_win = prediction()
print(any_win)
