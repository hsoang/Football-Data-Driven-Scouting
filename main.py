#Web Scraping
#Using mostly per 90 stats

from unidecode import unidecode
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
print(nameURL)

def normalize_name(name): #remove accents from names
    return unidecode(name)

data = requests.get(playerTest)
soup = BeautifulSoup(data.text, features = "html.parser")

Name = soup.find_all("span")
end = True
counter = 0

while (end):
    if nameURL in normalize_name(Name[counter].text):
        Name = Name[counter]
        end = False
    else:
        counter += 1

print(Name.text)


shortInfo = soup.find_all("p")
end = 0
while end < 5:
    if "Position" in shortInfo[end].text:
        shortInfo = shortInfo[end].text
        end = 5
    else:
        end += 1

#print(Position)
        
parts = shortInfo.split("▪ ")
Position = parts[0].split(":")[1].strip()
Footed = parts[1].split(":")[1].strip()

#print(f"His position is: {Position}")
#print(f"His dominant foot is: {Footed}")
    
Birthdate = soup.find_all("span", id = "necro-birth")
Birthdate = Birthdate[0].text
#print(Birthdate)

nationality = soup.find_all("p")
end = 0
while end < 5:
    if "National Team" in nationality[end].text:
        nationality = nationality[end].text
        end = 5
    else:
        end += 1

nationality = nationality.split(":")
NationalTeam = nationality[1].split(" ")
NationalTeam = NationalTeam[0].strip()
print(NationalTeam)


clubInfo = soup.find_all("p")
end = 0
while end < 7:
    if "Club:" in clubInfo[end].text:
        clubInfo= clubInfo[end].text
        end = 7
    else:
        end += 1


clubInfo = clubInfo.split(":")
Club = clubInfo[1].strip()
print(Club)

# stats_table = pd.read_html(data.text, match = "Scouting Report")
# print(stats_table)

stats = soup.find_all("tr")
print(stats[1].text)
print(stats[2].text)
print(stats[3].text)
print(stats[4].text)
print(stats[5].text)
print(stats[6].text)
print(stats[7].text)
print(stats[9].text)
print(stats[10].text)
print(stats[11].text)
print(stats[12].text)
print(stats[13].text)
print(stats[14].text)
print(stats[15].text)
print(stats[17].text)
print(stats[18].text)
print(stats[19].text)
print(stats[20].text)
print(stats[21].text)