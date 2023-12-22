#Football Web Scraping
#Using mostly per 90 stats

from unidecode import unidecode
import requests
from bs4 import BeautifulSoup
import json
import time
import re


def getTeamUrls():
    Ligue1 = "https://fbref.com/en/comps/13/Ligue-1-Stats"
    SerieA = "https://fbref.com/en/comps/11/Serie-A-Stats"
    LaLiga = "https://fbref.com/en/comps/12/La-Liga-Stats"
    Bundesliga = "https://fbref.com/en/comps/20/Bundesliga-Stats"
    Championship = "https://fbref.com/en/comps/10/Championship-Stats"
    Eredivisie = "https://fbref.com/en/comps/23/Eredivisie-Stats"

    leaguesList = [Ligue1]
    leaguesCount = len(leaguesList) #number of leagues to be used
    combinedLeaguesURLS = [] #urls of teams

   
    for x in range (leaguesCount): #Adds all the teams' URL
        data = requests.get(leaguesList[x])
        soup = BeautifulSoup(data.text, features = "html.parser")

        standings_table = soup.select('table', class_='stats_table')[0]

        
        links = standings_table.find_all('a')

        links = [l.get("href") for l in links]

        #print(links)

        links = [l for l in links if '/squads/' in l]

        #print(links)

        teamURLS = [f"https://fbref.com{l}" for l in links]
        combinedLeaguesURLS += teamURLS

    return combinedLeaguesURLS

#def    

def normalizeName(name): #remove accents from names
    name = name.replace("-"," ")
    return unidecode(name)

def retrievePlayerStats(teamLinks):
    playersNonGK = []
    playersGKs = []
    for x in range(len(teamLinks)):
        data = requests.get(teamLinks[x])
        soup = BeautifulSoup(data.text, features = "html.parser")

        stats_table = soup.select('table.stats_table')[0]

        links = stats_table.find_all('a')
        links = [l.get("href") for l in links]

        links = [l for l in links if "/players/" in l and "/matchlogs/" not in l]
        #print(links)

        playerURLS = [f"https://fbref.com{l}" for l in links] #urls of players
        #print(playerURLS)

        for x in range((len(playerURLS)) - 18): #Choosing number of players
            parts = playerURLS[x].split("/")
            name = parts[-1]
            nameURL = name.replace("-", " ")
            #print(nameURL)

            data = requests.get(playerURLS[x])
            soup = BeautifulSoup(data.text, features = "html.parser")

            Name = soup.find_all("span")
            end = True
            counter = 0

            while (end):
                if nameURL in normalizeName(Name[counter].text):
                    Name = Name[counter].text
                    end = False
                else:
                    counter += 1

            print(Name)
            shortInfo = soup.find_all("p")
            end = True
            counter = 0

            while (end):
                if "Position" in shortInfo[counter].text:
                    shortInfo = shortInfo[counter].text
                    end = False
                else:
                    counter += 1

            #print(Position, end = " ")
                    
            parts = shortInfo.split("▪ ")
            Position = parts[0].split(":")[1].strip()
            try:
                Footed = parts[1].split(":")[1].strip()
            except IndexError:
                Footed = None

            print(Position)
            if (Footed == None):
                pass
            else:
                print(Footed)
                
            Birthdate = soup.find_all("span", id = "necro-birth")
            Birthdate = Birthdate[0].text
            Birthdate = Birthdate.strip()
            print(Birthdate)

            nationality = soup.find_all("p")
            end = True
            counter = 0

            while (end):
                if "National Team" in nationality[counter].text or "Citizenship" in nationality[counter].text:
                    nationality = nationality[counter].text
                    end = False
                else:
                    counter += 1

            nationality = nationality.split(":")
            NationalTeam = nationality[1].split(" ")
            NationalTeam = NationalTeam[0].strip()
            print(NationalTeam)


            clubInfo = soup.find_all("p")
            end = True
            counter = 0

            while (end):
                if "Club:" in clubInfo[counter].text:
                    clubInfo= clubInfo[counter].text
                    end = False
                else:
                    counter += 1


            clubInfo = clubInfo.split(":")
            Club = clubInfo[1].strip()
            print(Club)

            if "GK" in Position:
                stats = soup.find_all("tr")
                stat1 = stats[1].text
                # stat1 = stat1[8:]
                print(stat1)
                # print(stats[2].text)
                # print(stats[3].text)
                # print(stats[4].text)
                # print(stats[5].text)
            else:
                stats = soup.find_all("tr")
                stat1 = stats[1].text
                # stat1 = stat1[17:]
                print(stat1)
                # print(stats[2].text)
                # print(stats[3].text)
                # print(stats[4].text)
                # print(stats[5].text)


            time.sleep(3)

    return playersNonGK, playersGKs


if __name__ == '__main__':
    print("main")

    teamUrls = getTeamUrls()
    #print(teamUrls)
    
    NonGKs, GKs = retrievePlayerStats(teamUrls[0:1])