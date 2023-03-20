# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 11:03:28 2023

@author: adama
"""
# file="C:/Users/adama/OneDrive/02_MPH/01_Python/WorldCupGoals.csv"
# print(file)
# importing all the required addons
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
fifa_head=fifa.head()#looks at the head
fifa_info=fifa.info()#looks at the info
fifa_with_firstname=fifa.dropna()
fifa=fifa.fillna('noname')
fifa[['match_name','away']]=fifa['match_name'].str.split(" v ", expand = True)#splits the 'match_name into 2 columns, using the v as the deliminater 
fifa['match_date']=pd.to_datetime(fifa['match_date'], dayfirst=True)#changes the match date into date-time format
fifa_Brazil = fifa[fifa["player_team_name"] == "Brazil"]#shows only the brazil goals
is_Brazil = fifa["player_team_name"] == "Brazil"#creats
is_Final = fifa["stage_name"] == "final"
fifa_Brazil_Final = fifa[is_Brazil & is_Final]
fifa_scoreextratime = fifa[fifa["minute_regulation"] >90]

both = fifa.merge(pop, left_on='team_name', right_on='Country (or dependency)') 
both['goal']=1

both_sort_team = both.groupby(["player_team_name"]).sum()#sorting data by teams and then suming the data
both_sort_team['Population (2020)']=both_sort_team['Population (2020)']/both_sort_team['goal'] # as the last one "summed all the populations, this gets it back to actual population
plt.scatter(both_sort_team['Population (2020)'],both_sort_team['goal'])# graph pop vs number ofo goals to see if pop affects the number of goals
plt.xlabel('Population (x10^8)')# adding x, y and titlas to the code
plt.ylabel('Total Goals')
plt.title('Total Goals per Population')
plt.show()

both_total_goals_per_yr = both.groupby([both.match_date.dt.year]).agg(totalgoals=('goal','sum'))#sum the total goals per year
plt.scatter(both_total_goals_per_yr.index, both_total_goals_per_yr['totalgoals'])#plotting a scatter plot of the previous line
plt.xlabel('Year')# adding x, y and titlas to the code
plt.ylabel('Total Goals')
plt.title('Total Goals per Worldcup')
plt.show()

fifa_finalgoals= fifa[fifa["stage_name"] == "final"]#golas that were scored in the final 
fifa_finalgoals['goal']=1#adding a new column that can be used to sum "number of goals"

tournaments =fifa_finalgoals['tournament_id'].drop_duplicates()#leaves a list of tournaments
length = len(tournaments)# how many tournaments was there
fifa_final_winners_df = pd.DataFrame(columns=['Tournament', 'Home_Team', 'Away_Team', 'Home_Goals', 'Away_Goals', 'Winner', 'Wins'])# a new 'emepty dataframe

for i in range(length):#start of 'for' loop, repeating fo rhte amount the tournaments there was
    
    tourn1 = tournaments.iloc[i] #picks ou the tournment name, changing with each loop
    
    tourn= fifa_finalgoals[fifa_finalgoals['tournament_id']==tourn1]# returning only the results from selected world cup
    a=tourn.sum()#number of goals scored in the final
    bhometeam = tourn['match_name'].iloc[0]#goals socred by the home and away teams
    bawayteam = tourn['away'].iloc[0]
    aawaygoals=a['away_team']
    ahomegoals=a['home_team']
    if aawaygoals > ahomegoals:#defins the sinner, else if its a draw (anfter extra time) it defines that. 
            winner = bawayteam
    elif aawaygoals < ahomegoals:
            winner = bhometeam
    elif aawaygoals == ahomegoals:
            winner = 'went to penos'          
    fifa_final_winners = [tourn1, bhometeam, bawayteam,  ahomegoals, aawaygoals, winner, 1]#creates a list of the reults collected
    fifa_final_winners_df.loc[len(fifa_final_winners_df)]=fifa_final_winners#feeds previous list into a dataframe
    #print(fifa_final_winners)
    #fifa_final_winners_df.groupby('Winner')['Wins'].sum('Wins').plot.bar()
fifa_final_winners_df_totalwins=fifa_final_winners_df.groupby('Winner')['Wins'].sum('Wins')#groups total wins, and gaphs them
fifa_final_winners_df_totalwins.plot.bar()
plt.xlabel('Country')
plt.ylabel('Total Wins')
plt.title('Total Wins per Country')
plt.show()

#Players with no first names

#fifa_with_firstname=fifa.dropna()
#fifa_with_firstname_info=fifa_with_firstname.info()
#fifa=fifa.fillna('noname')
#https://api.nationalize.io?name=nathaniel


topscorer = both.groupby(["family_name",'given_name'])['goal'].sum()#uses the family and given name to find the number of goals scored by a player. 
topscorer_name = topscorer.idxmax()#finds the top scorer
topscorer_firstname = topscorer_name[1]
topscorer_top5=topscorer.sort_values(ascending=False).head()
print(topscorer_top5)
#a = national_pd['country'][0]['country_id'], national_pd['country'][0]['probability']
is_givenname = fifa["given_name"] == topscorer_name[1]
is_familyname = fifa["family_name"] == topscorer_name[0]
fifa_topscorer = fifa[is_familyname & is_givenname]
fifa_topscorer_national = fifa_topscorer.iloc[0]['team_name']

web = 'https://api.nationalize.io?name='#creates variable for the API link
web2 = web + topscorer_firstname#creates variable adnd link for top scorer
nationality = requests.get(web2)#requests data from ap 
national_pd =pd.DataFrame(nationality.json())#converts API to DF

national_markup= pd.DataFrame(columns=['country', 'probability'])#pulls out nationality and graphs the results
for i in range(len(national_pd)):
    a = national_pd['country'][i]['country_id'], national_pd['country'][i]['probability']
    national_markup.loc[len(national_markup)]=a
national_markup.plot.bar(x='country', y='probability')
plt.xlabel('Country')
plt.ylabel('Prob')
#plt.title('The most goals scored in the world cup was ' + topscorer_name[0] + ' ' +topscorer_name[1] +',he scored' +topscorrer.max()+ 'goals for ' + fifa_topscorer_national ',but he may be from')
plt.title('The most goals scored in the world cup was ' + topscorer_name[1] + ' ' +topscorer_name[0] +',he scored ' + str(topscorer.max()) + ' goals for ' + fifa_topscorer_national +',but he may be from')
plt.show()# shows thwe grapgh with the dynamic title

def numberofgoals(country,tournament):# creates function
    is_country = fifa["player_team_name"] == country#creats
    is_tourn = fifa["tournament_id"] == tournament
    fifa_country_tourn = fifa[is_country & is_tourn]
    goals = country +' scored ' + str(len(fifa_country_tourn)) + ' goals in ' + tournament
    return goals
    print(fifa_country_tourn)

goals_in_tounament=numberofgoals('Brazil','WC-1930')#call functions are the diffect variables
print(goals_in_tounament)

goals_in_tounament=numberofgoals('Uruguay','WC-1954')
print(goals_in_tounament)


    
    
    
    
