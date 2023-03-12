# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 11:03:28 2023

@author: adama
"""
# file="C:/Users/adama/OneDrive/02_MPH/01_Python/WorldCupGoals.csv"
# print(file)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import requests

file= r'C:/Users/adam.agnew/OneDrive/02_MPH/01_Python/WorldCupGoals.csv'
#file=r'C:/Users/adam.agnew/Desktop/WorldCupGoals.csv'
#set the file as World Cup goals
fifa=pd.read_csv(file, encoding = "ISO-8859-1")
#import with encoding as there are player names with special characters. 
file2 = r'C:/Users/adam.agnew/OneDrive/02_MPH/01_Python/population_by_country_2020.csv'
#file2 = r'C:/Users/adam.agnew/Desktop/population_by_country_2020.csv'
pop = pd.read_csv(file2)
#fifa=pd.read_csv(r'C:/Users/adam.agnew/Desktop/WorldCupGoals.csv')
#print(fifa)
fifa_head=fifa.head()
fifa_info=fifa.info()
fifa[['match_name','away']]=fifa['match_name'].str.split(" v ", expand = True)
fifa['match_date']=pd.to_datetime(fifa['match_date'], dayfirst=True)
fifa_Brazil = fifa[fifa["player_team_name"] == "Brazil"]
fifa_no_name = fifa[fifa["given_name"] == "not applicable"]
is_Brazil = fifa["player_team_name"] == "Brazil"
is_Final = fifa["stage_name"] == "final"
fifa_Brazil_Final = fifa[is_Brazil & is_Final]
fifa_scoreextratime = fifa[fifa["minute_regulation"] >90]

both = fifa.merge(pop, left_on='team_name', right_on='Country (or dependency)') 
both['goal']=1

test = both.groupby(["player_team_name"]).sum()#sorting data by teams and then suming the data
test['Population (2020)']=test['Population (2020)']/test['goal'] # as the last one "summed all the populations, this gets it back to actual population
#plt.scatter(test['Population (2020)'],test['goal'])# graph pop vs number ofo goals to see if pop affects the number of goals

test2 = both.groupby([both.match_date.dt.year]).agg(totalgoals=('goal','sum'))
plt.scatter(test2.index, test2['totalgoals'])
plt.xlabel('Year')
plt.ylabel('Total Goals')
plt.title('Total Goals per Worldcup')
plt.show()

fifa_finalgoals= fifa[fifa["stage_name"] == "final"]
fifa_finalgoals['goal']=1

tournaments =fifa_finalgoals['tournament_id'].drop_duplicates()
length = len(tournaments)
fifa_final_winners_df = pd.DataFrame(columns=['Tournament', 'Home_Team', 'Away_Team', 'Home_Goals', 'Away_Goals', 'Winner', 'Wins'])

for i in range(length):
    
    toun1 = tournaments.iloc[i]
    
    tourn= fifa_finalgoals[fifa_finalgoals['tournament_id']==toun1]
    a=tourn.sum()
    bhometeam = tourn['match_name'].iloc[0]
    bawayteam = tourn['away'].iloc[0]
    aawaygoals=a['away_team']
    ahomegoals=a['home_team']
    if aawaygoals > ahomegoals:
            winner = bawayteam
    elif aawaygoals < ahomegoals:
            winner = bhometeam
    elif aawaygoals == ahomegoals:
            winner = 'went to penos'          
    fifa_final_winners = [toun1, bhometeam, bawayteam,  ahomegoals, aawaygoals, winner, 1]
    fifa_final_winners_df.loc[len(fifa_final_winners_df)]=fifa_final_winners
    #print(fifa_final_winners)
    #fifa_final_winners_df.groupby('Winner')['Wins'].sum('Wins').plot.bar()
fifa_final_winners_df_totalwins=fifa_final_winners_df.groupby('Winner')['Wins'].sum('Wins')
fifa_final_winners_df_totalwins.plot.bar()

#Players with no first names

fifa_with_firstname=fifa.dropna()
#fifa_with_firstname_info=fifa_with_firstname.info()

#https://api.nationalize.io?name=nathaniel


topscorer = both.groupby(["family_name",'given_name'])['goal'].sum()
topscorer_name = topscorer.idxmax()
topscorer_firstname = topscorer_name[1]
web = 'https://api.nationalize.io?name='
web2 = web + topscorer_firstname
#topscorer = topscorer.sort_values(ascending=False)
#nationality = requests.get(web2).content
nationality = requests.get(web2)
national_pd =pd.DataFrame(nationality.json())

#a = national_pd['country'][0]['country_id'], national_pd['country'][0]['probability']
is_givenname = fifa["given_name"] == topscorer_name[1]
is_familyname = fifa["family_name"] == topscorer_name[0]
fifa_topscorer = fifa[is_familyname & is_givenname]
fifa_topscorer_national = fifa_topscorer.iloc[0]['team_name']

national_markup= pd.DataFrame(columns=['country', 'probability'])
for i in range(len(national_pd)):
    a = national_pd['country'][i]['country_id'], national_pd['country'][i]['probability']
    national_markup.loc[len(national_markup)]=a
national_markup.plot.bar(x='country', y='probability')
plt.xlabel('Country')
plt.ylabel('Prob')
#plt.title('The most goals scored in the world cup was ' + topscorer_name[0] + ' ' +topscorer_name[1] +',he scored' +topscorrer.max()+ 'goals for ' + fifa_topscorer_national ',but he may be from')
plt.title('The most goals scored in the world cup was ' + topscorer_name[0] + ' ' +topscorer_name[1] +',he scored ' + str(topscorer.max()) + ' goals for ' + fifa_topscorer_national +',but he may be from')
plt.show()
    
