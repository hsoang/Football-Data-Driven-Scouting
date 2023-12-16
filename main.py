#Web Scraping
#Using mostly per 90 stats

import requests
from bs4 import BeautifulSoup
import pandas as pd



Big5 = "https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats#all_big5_table"
Championship = "https://fbref.com/en/comps/10/Championship-Stats"
Eredivisie = "https://fbref.com/en/comps/23/Eredivisie-Stats"

leaguesCount = 3 #number of leagues to be used
leaguesList = [Big5,Championship,Eredivisie]
combinedLeaguesURLS = [] #urls of teams

for x in range (leaguesCount): #Adds all the teams' URL
    data = requests.get(leaguesList[x])

    soup = BeautifulSoup(data.text, features = "html.parser")
    standings_table = soup.select('table.stats_table')[0]

    links = standings_table.find_all('a')

    links = [l.get("href") for l in links]

    #print(links)

    links = [l for l in links if '/squads/' in l]

    #print(links)

    teamURLS = [f"https://fbref.com{l}" for l in links]
    combinedLeaguesURLS += teamURLS
    

#print(combinedLeaguesURLS)
team_url = combinedLeaguesURLS[0]
#print(team_url)
data = requests.get(team_url)

soup = BeautifulSoup(data.text, features = "html.parser")
stats_table = soup.select('table.stats_table')[0]

links = stats_table.find_all('a')
links = [l.get("href") for l in links]

links = [l for l in links if "/players/" in l and "/matchlogs/" not in l]
#print(links)

playerURL = [f"https://fbref.com{l}" for l in links] #urls of players
#print(playerURL)

playerTest = playerURL[9]
#print(playerTest)


parts = playerTest.split("/")
name = parts[-1]
nameURL = name.replace("-", " ")
#print(nameURL)


data = requests.get(playerTest)
soup = BeautifulSoup(data.text, features = "html.parser")

Name = soup.find_all("span")
Name = [N for N in Name if nameURL in N]
print(Name[0].text)

Position = soup.find_all("p")
end = 0
while end < 10:
    if "Position" in Position[end].text:
        Position = Position[end].text
        end = 10
    else:
        end += 1
    




# Position = [P for P in Position if "Position:" in P]
#print(Position)
# Footed =
# Nationality =








