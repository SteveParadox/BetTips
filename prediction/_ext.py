#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/SteveParadox/Organizer-Automator/blob/main/_ext.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[42]:


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


# In[43]:


urls = [
    "https://www.goal.com/en-us/premier-league/table/6wubmo7di3kdpflluf6s8c7vs",
    "https://www.goal.com/en-us/ligue-1/table/57nu0wygurzkp6fuy5hhrtaa2",
    "https://www.goal.com/en-us/liga-profesional-argentina/table/581t4mywybx21wcpmpykhyzr3",
    "https://www.goal.com/en-us/a-league-men/table/xwnjb1az11zffwty3m6vn8y6",
    "https://www.goal.com/en-us/first-division-a/table/4zwgbb66rif2spcoeeol2motx",
    "https://www.goal.com/en-us/premijer-liga/table/4yngyfinzd6bb1k7anqtqs0wt",
    "https://www.goal.com/en-us/serie-a/table/scf9p4y91yjvqvg5jndxzhxj",
    "https://www.goal.com/en-us/primera-divisi%C3%B3n/table/2y8bntiif3a9y6gtmauv30gt",
    "https://www.goal.com/en-us/primera-b/table/bly7ema5au6j40i0grhl0pnub",
    "https://www.goal.com/en-us/csl/table/82jkgccg7phfjpd0mltdl3pat",
    "https://www.goal.com/en-us/primera-a/table/2ty8ihceabty8yddmu31iuuej",
    "https://www.goal.com/en-us/primera-b/table/by5nibd18nkt40t0j8a0j5yzx",
    "https://www.goal.com/en-us/hnl/table/1b70m6qtxrp75b4vtk8hxh8c3",
    "https://www.goal.com/en-us/czech-liga/table/bu1l7ckihyr0errxw61p0m05",
    "https://www.goal.com/en-us/superliga/table/29actv1ohj8r10kd9hu0jnb0n",
    "https://www.goal.com/en-us/liga-pro/table/6lwpjhktjhl9g7x2w7njmzva6",
    "https://www.goal.com/en-us/premier-league/table/8k1xcsyvxapl4jlsluh3eomre",
    "https://www.goal.com/en-us/championship/table/7ntvbsyq31jnzoqoa8850b9b8",
    "https://www.goal.com/en-us/league-one/table/3frp1zxrqulrlrnk503n6l4l",
    "https://www.goal.com/en-us/premier-league/table/2kwbbcootiqqgmrzs6o5inle5",
    "https://www.goal.com/en-us/league-two/table/bgen5kjer2ytfp7lo9949t72g",
    "https://www.goal.com/en-us/premier-league-2-division-one/table/75434tz9rc14xkkvudex742ui",
    "https://www.goal.com/en-us/premier-league-2-division-two/table/a0zpsx4vvgvn2kpxzg1bcciui",
    "https://www.goal.com/en-us/ligue-1/table/dm5ka0os1e3dxcp3vh05kmp33",
    "https://www.goal.com/en-us/ligue-2/table/4w7x0s5gfs5abasphlha5de8k",
    "https://www.goal.com/en-us/bundesliga/table/6by3h89i2eykc341oz7lv1ddd",
    "https://www.goal.com/en-us/2-bundesliga/table/722fdbecxzcq9788l6jqclzlw",
    "https://www.goal.com/en-us/premier-league/table/4jg7he1n3rb5dniq6hf49xorq",
    "https://www.goal.com/en-us/super-league-1/table/c0r21rtokgnbtc0o2rldjmkxu",
    "https://www.goal.com/en-us/premier-league/table/4rls982p5uzil6x30mhyhv9f3",
    "https://www.goal.com/en-us/nb-i/table/47s2kt0e8m444ftqvsrqa3bvq",
    "https://www.goal.com/en-us/nb-ii/table/beqqnubkv05mamuwvimeum015",
    "https://www.goal.com/en-us/indian-super-league/table/3oa9e03e7w9nr8kqwqc3tlqz9",
    "https://www.goal.com/en-us/i-league/table/4pohvulrkgzx38eoqse6b5cdg",
    "https://www.goal.com/en-us/isc-a/table/253foz8zjbecgiyhz4cgytxih",
    "https://www.goal.com/en-us/liga-1/table/117yqo02rs8dykkxpm274w3bd",
    "https://www.goal.com/en-us/serie-a/table/1r097lpxe0xn03ihb7wi98kao",
    "https://www.goal.com/en-us/fkf-premier-league/table/7wssxdqi4xihseeam8grqa2b8",
    "https://www.goal.com/en-us/j2-league/table/5z8v4mj6cjs9ex6hdrpourjzh",
    "https://www.goal.com/en-us/serie-b/table/8ey0ww2zsosdmwr8ehsorh6t7",
    "https://www.goal.com/en-us/serie-c/table/1zp1du9n4rj36p1ss9zbxtqfb",
    "https://www.goal.com/en-us/j1-league/table/8o5tv5viv4hy1qg9jp94k7ayb",
    "https://www.goal.com/en-us/super-league/table/eg6s9f1jj7jr6stmbosn0g6c8",
    "https://www.goal.com/en-us/liga-mx/table/2hsidwomhjsaaytdy9u5niyi4",
    "https://www.goal.com/en-us/botola-pro/table/1eruend45vd20g9hbrpiggs5u",
    "https://www.goal.com/en-us/eerste-divisie/table/1gwajyt0pk2jm5fx5mu36v114",
    "https://www.goal.com/en-us/eredivisie/table/akmkihra9ruad09ljapsm84b3",
    "https://www.goal.com/en-us/eliteserien/table/9ynnnx1qmkizq1o3qr3v0nsuk",
    "https://www.goal.com/en-us/division-profesional/table/5y0z0l2epprzbscvzsgldw8vu",
    "https://www.goal.com/en-us/primera-divisi%C3%B3n/table/a9vrdkelbgif0gtu3wxsr75xo",
    "https://www.goal.com/en-us/ekstraklasa/table/7hl0svs2hg225i2zud0g3xzp2",
    "https://www.goal.com/en-us/primeira-liga/table/8yi6ejjd1zudcqtbn07haahg6",
    "https://www.goal.com/en-us/stars-league/table/xaouuwuk8qyhv1libkeexwjh",
    "https://www.goal.com/en-us/liga-i/table/89ovpy1rarewwzqvi30bfdr8b",
    "https://www.goal.com/en-us/saudi-league/table/ea0h6cf3bhl698hkxhpulh2zz",
    "https://www.goal.com/en-us/championship/table/8t2o4huu2e48ij23dxnl9w5qx",
    "https://www.goal.com/en-us/league-one/table/6sxm2iln2w45ux498pty9miw8",
    "https://www.goal.com/en-us/league-two/table/6321dlqv4ziuwqte4xpohijtw",
    "https://www.goal.com/en-us/premiership/table/e21cf135btr8t3upw0vl6n6x0",
    "https://www.goal.com/en-us/psl/table/yv73ms6v1995b5wny16jcfi3",
    "https://www.goal.com/en-us/primera-divisi%C3%B3n/table/34pl8szyvrbwcmfkuocjm3r6t",
    "https://www.goal.com/en-us/segunda-divisi%C3%B3n/table/3is4bkgf3loxv9qfg3hm8zfqb",
    "https://www.goal.com/en-us/sudani-premier-league/table/2c01jrik7ggtta321pstz8tm4",
    "https://www.goal.com/en-us/allsvenskan/table/b60nisd3qn427jm0hrg9kvmab",
    "https://www.goal.com/en-us/super-league/table/e0lck99w8meo9qoalfrxgo33o",
    "https://www.goal.com/en-us/ligi-kuu-bara/table/9z5643nd06afqu01ea2wt8y4g",
    "https://www.goal.com/en-us/thai-league-1/table/iu1vi94p4p28oozl1h9bvplr",
    "https://www.goal.com/en-us/thai-league-2/table/bt24epydr1s8zc2x5xb0n9noc",
    "https://www.goal.com/en-us/1-lig/table/2o9svokc5s7diish3ycrzk7jm",
    "https://www.goal.com/en-us/s%C3%BCper-lig/table/482ofyysbdbeoxauk19yg7tdt",
    "https://www.goal.com/en-us/pro-league/table/f39uq10c8xhg5e6rwwcf6lhgc",
    "https://www.goal.com/en-us/mls/table/287tckirbfj9nb8ar2k9r60vn",
    "https://www.goal.com/en-us/vleague-1/table/aho73e5udydy96iun3tkzdzsi",
    "https://www.goal.com/en-us/premier-soccer-league/table/4azsryi40zahspm5h6d0f0pgl"

]
print(len(urls))


# In[44]:
urls = urls[:5]

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


# In[45]:


data = teams()
print(len(data))


# In[46]:


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


# In[49]:
def write_to_txt(data, filename):
    try:
        with open(filename, 'w') as file:
            for item in data:
                file.write(f"{item}\n")
        print(f"Data written to {filename} successfully.")
    except Exception as e:
        print(f"Error writing to {filename}: {e}")



def prediction():
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
        
        write_to_txt(for_team, './Site/Output_Data/for_team.txt')
        write_to_txt(against_team, './Site/Output_Data/against_team.txt')
        write_to_txt(any_win, './Site/Output_Data/any_win.txt')


        return for_team, against_team, any_win

    except Exception as e:
        print(f"Error: {e}")
        return None
# In form team, Teams to bet against


# In[50]:


for_team, against_team, any_win = prediction()
print(any_win)


# In[152]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

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



# In[153]:


print(len(match_fix))


# In[154]:


# Getting the fixtures of the already predicted teams

import numpy as np

def get_fixtures(match_fix):
    for_team, against_team, any_win = prediction()

    match_fix = np.array(match_fix)
    selection_set = np.array([line.strip() for line in for_team])
    compiled_for = np.array([item for item in match_fix if np.any(np.isin(item.split(' vs '), selection_set))] )

    selection_set_against = np.array([line.strip() for line in against_team])
    compiled_against = np.array([item for item in match_fix if np.any(np.isin(item.split(' vs '), selection_set_against))])

    selection_set_any = np.array([line.strip() for line in any_win])
    compiled_any = np.array([item for item in match_fix if np.any(np.isin(item.split(' vs '), selection_set_any))])

    return compiled_for, compiled_against, compiled_any

    """except Exception as e:
        print(f"Error: {e}")
        return None """


# In[155]:


compiled_for, compiled_against, compiled_any = get_fixtures(match_fix)
print(compiled_for)
print(compiled_against)
print(compiled_any)


# In[131]:


compiled_for = {match for match in compiled_for if 'Ladies' not in match and 'Women' not in match}
compiled_against = {match for match in compiled_against if 'Ladies' not in match and 'Women' not in match}
compiled_any = {match for match in compiled_any if 'Ladies' not in match and 'Women' not in match}

compiled_for = [[s.strip() for s in item.split('vs')] for item in compiled_for]
compiled_against = [[s.strip() for s in item.split('vs')] for item in compiled_against]
compiled_any = [[s.strip() for s in item.split('vs')] for item in compiled_any]

print(compiled_for)
print(compiled_against)
print(compiled_any)
# weekly Prediction


# In[56]:


print(dff['GF'])


# In[132]:


def high_gf_ga():
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
    
    write_to_txt(high_scoring_teams, './Site/Output_Data/high_scoring_teams.txt')
    write_to_txt(high_conceding_teams, './Site/Output_Data/high_conceding_teams.txt')



    return high_scoring_teams, high_conceding_teams, threshold_high_goal_scoring

# High Scoring Teams / High conceding


# In[133]:


high_scoring_teams, high, threshold_high_goal_scoring= high_gf_ga()
print(high_scoring_teams)
print(high)


# In[134]:


compiled = compiled_for + compiled_against + compiled_any
print (threshold_high_goal_scoring)


# In[151]:


def predict_both_teams_score(compiled, threshold_high_goal_scoring):
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
    
    write_to_txt(predictions, './Site/Output_Data/bts_predictions.txt')
    
    return predictions

predictions = predict_both_teams_score(compiled, threshold_high_goal_scoring)
print(predictions)

