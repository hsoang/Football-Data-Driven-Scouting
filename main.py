#Web Scraping
#Using mostly per 90 stats

from unidecode import unidecode
import requests
from bs4 import BeautifulSoup
import pandas as pd


def getTeamUrls():
    Ligue1 = "https://fbref.com/en/comps/13/Ligue-1-Stats"
    SerieA = "https://fbref.com/en/comps/11/Serie-A-Stats"
    LaLiga = "https://fbref.com/en/comps/12/La-Liga-Stats"
    Bundesliga = "https://fbref.com/en/comps/20/Bundesliga-Stats"
    Championship = "https://fbref.com/en/comps/10/Championship-Stats"
    Eredivisie = "https://fbref.com/en/comps/23/Eredivisie-Stats"

    leaguesList = [SerieA]
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
    


# #print(combinedLeaguesURLS)
# team_url = combinedLeaguesURLS[3]
# #print(team_url)
# data = requests.get(team_url)
# soup = BeautifulSoup(data.text, features = "html.parser")

# stats_table = soup.select('table', class_='stats_table')[0]

# links = stats_table.find_all('a')
# links = [l.get("href") for l in links]

# links = [l for l in links if "/players/" in l and "/matchlogs/" not in l]
# #print(links)

# playerURL = [f"https://fbref.com{l}" for l in links] #urls of players
# #print(playerURL)

# # playerTest = playerURL[1]
# # print(playerTest)
# #print(len(playerURL))

# def normalize_name(name): #remove accents from names
#     name = name.replace("-"," ")
#     return unidecode(name)

# for x in range(len(playerURL)):
#     parts = playerURL[x].split("/")
#     name = parts[-1]
#     nameURL = name.replace("-", " ")
#     print(nameURL)

#     data = requests.get(playerURL[x])
#     soup = BeautifulSoup(data.text, features = "html.parser")
#     Name = soup.find_all("span")
#     end = True
#     counter = 0

#     while (end):
#         if nameURL in normalize_name(Name[counter].text):
#             Name = Name[counter]
#             end = False
#         else:
#             counter += 1

#     print(Name.text)

# data = requests.get(playerURL[x])
# soup = BeautifulSoup(data.text, features = "html.parser")

# Name = soup.find_all("span")
# end = True
# counter = 0

# while (end):
#     if nameURL in normalize_name(Name[counter].text):
#         Name = Name[counter]
#         end = False
#     else:
#         counter += 1

# print(Name.text)


# shortInfo = soup.find_all("p")
# end = 0
# while end < 5:
#     if "Position" in shortInfo[end].text:
#         shortInfo = shortInfo[end].text
#         end = 5
#     else:
#         end += 1

# #print(Position)
        
# parts = shortInfo.split("▪ ")
# Position = parts[0].split(":")[1].strip()
# Footed = parts[1].split(":")[1].strip()

# #print(f"His position is: {Position}")
# #print(f"His dominant foot is: {Footed}")
    
# Birthdate = soup.find_all("span", id = "necro-birth")
# Birthdate = Birthdate[0].text
# #print(Birthdate)

# nationality = soup.find_all("p")
# end = 0
# while end < 5:
#     if "National Team" in nationality[end].text:
#         nationality = nationality[end].text
#         end = 5
#     else:
#         end += 1

# nationality = nationality.split(":")
# NationalTeam = nationality[1].split(" ")
# NationalTeam = NationalTeam[0].strip()
# print(NationalTeam)


# clubInfo = soup.find_all("p")
# end = 0
# while end < 7:
#     if "Club:" in clubInfo[end].text:
#         clubInfo= clubInfo[end].text
#         end = 7
#     else:
#         end += 1


# clubInfo = clubInfo.split(":")
# Club = clubInfo[1].strip()
# print(Club)


# stats = soup.find_all("tr")
# print(stats[1].text)
# print(stats[2].text)
# print(stats[3].text)
# print(stats[4].text)
# print(stats[5].text)
# print(stats[6].text)
# print(stats[7].text)
# print(stats[9].text)
# print(stats[10].text)
# print(stats[11].text)
# print(stats[12].text)
# print(stats[13].text)
# print(stats[14].text)
# print(stats[15].text)
# print(stats[17].text)
# print(stats[18].text)
# print(stats[19].text)
# print(stats[20].text)
# print(stats[21].text)

def normalizeName(name): #remove accents from names
    name = name.replace("-"," ")
    return unidecode(name)

def retrievePlayerStats(teamLinks):
    
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

        for x in range((len(playerURLS)) - 18):
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
                if "Position" in shortInfo[end].text:
                    shortInfo = shortInfo[end].text
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

            print(Position, end = " ")
            if (Footed == None):
                pass
            else:
                print(f"Dominant foot is: {Footed}", end = " ")
                
            Birthdate = soup.find_all("span", id = "necro-birth")
            Birthdate = Birthdate[0].text
            print(Birthdate, end = " ")

            nationality = soup.find_all("p")
            end = True
            counter = 0

            while (end):
                if "National Team" in nationality[end].text:
                    nationality = nationality[end].text
                    end = False
                else:
                    counter += 1

            nationality = nationality.split(":")
            NationalTeam = nationality[1].split(" ")
            NationalTeam = NationalTeam[0].strip()
            print(NationalTeam, end = " ")


            clubInfo = soup.find_all("p")
            end = True
            counter = 0

            while (end):
                if "Club:" in clubInfo[end].text:
                    clubInfo= clubInfo[end].text
                    end = False
                else:
                    counter += 1


            clubInfo = clubInfo.split(":")
            Club = clubInfo[1].strip()
            print(Club)


if __name__ == '__main__':
    print("main")

    teamUrls = getTeamUrls()
    #print(teamUrls)
    
    retrievePlayerStats(teamUrls)