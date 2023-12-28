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

def createPlayerObjectNonGK(name, position, footed, birthdate, nationality,
                            club, stat1, stat2, stat3, stat4, stat5, stat6, stat7,
                              stat9, stat10, stat11, stat12, stat14,
                              stat15, stat17, stat18, stat19, stat20, stat21):
    new_player = {
        "name": name,
        "position": position,
        "footed": footed,
        "birthdate": birthdate,
        "nationality": nationality,
        "club" : club,
        "Non-Penalty Goals": stat1,
        "Non-Penalty xG(npxG)": stat2,
        "Shots Total": stat3,
        "Assists": stat4,
        "Expected Asissted Goals(xAG)": stat5,
        "npxG + xAG": stat6,
        "Shot-Creating Actions": stat7,
        "Passes Attempted": stat9,
        "Pass Completion %": stat10,
        "Progessive Passes": stat11,
        "Progessive Carries": stat12,
        "Successful Take-Ons": stat14,
        "Touches(Att Pen)": stat15,
        "Tackles": stat17,
        "Interceptions": stat18,
        "Blocks": stat19,
        "Clearances": stat20,
        "Aerials Won": stat21
    }
    return new_player

def createPlayerObjectGK(name, position, footed, birthdate, nationality, club, stat1, stat2, stat3, stat4, stat5,
                         stat6, stat8, stat9, stat10, stat11, stat13, stat14, stat15):
    new_player = {
        "name": name,
        "position": position,
        "footed": footed,
        "birthdate": birthdate,
        "nationality": nationality,
        "club": club,
        "Post-Shot Expected Goals minus Goals Allowed": stat1,
        "Goals Against": stat2,
        "Save Percentage": stat3,
        "Post-Shot Expected Goals per Shot on Target": stat4,
        "Saves% (Penality Kicks)": stat5,
        "Clean Sheet Percentage": stat6,
        "Touches": stat8,
        "Launch %": stat9,
        "Goal Kicks": stat10,
        "Average length of Goal Kicks": stat11,
        "Crosses Stopped %": stat13,
        "Defensive Actions Outside Penalty Area": stat14,
        "Average Distance of Defense Actions": stat15
    }
    return new_player


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

        for x in range((len(playerURLS)) - 24): #Choosing number of players
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

            #print(Name, end = " ")
            shortInfo = soup.find_all("p")
            end = True
            counter = 0

            while (end):
                if "Position" in shortInfo[counter].text:
                    shortInfo = shortInfo[counter].text
                    end = False
                else:
                    counter += 1

           
                    
            parts = shortInfo.split("▪ ")
            Position = parts[0].split(":")[1].strip()
            try:
                Footed = parts[1].split(":")[1].strip()
            except IndexError:
                Footed = None

            #print(Position, end = " ")
            # if (Footed == None):
            #     pass
            # else:
            #     print(Footed)
                
            Birthdate = soup.find_all("span", id = "necro-birth")
            Birthdate = Birthdate[0].text
            Birthdate = Birthdate.strip()
            #print(Birthdate)

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
            #print(NationalTeam, end = " ")


            clubInfo = soup.find_all("p")
            end = True
            counter = 0

            while (end):
                if "Club:" in clubInfo[counter].text:
                    clubInfo = clubInfo[counter].text
                    end = False
                else:
                    counter += 1


            clubInfo = clubInfo.split(":")
            Club = clubInfo[1].strip()
            #print(Club)

            if "GK" in Position:
                #print(Name)
                stats = soup.find_all("tr")
                stat1 = stats[1].text
                stat1 = stat1[7:12]
                #print(stat1)
                stat2 = stats[2].text
                stat2 = stat2[13:17]
                #print(stat2)
                stat3 = stats[3].text
                stat3 = stat3[15:19]
                #print(stat3)
                stat4 = stats[4].text
                stat4 = stat4[8:12]
                #print(stat4)
                stat5 = stats[5].text
                stat5 = stat5[21:25]
                #print(stat5)
                stat6 = stats[6].text
                stat6 = stat6[22:26]
                #print(stat6)
                stat8 = stats[8].text
                stat8 = stat8[7:12]                
                #print(stat8)
                stat9 = stats[9].text
                stat9 = stat9[8:13]               
                #print(stat9)
                stat10 = stats[10].text
                stat10 = stat10[10:14]                
                #print(stat10)
                stat11 = stats[11].text
                stat11 = stat11[25:29]
                #print(stat11)
                stat13 = stats[13].text
                stat13 = stat13[17:21]
                #print(stat13)
                stat14 = stats[14].text
                stat14 = stat14[30:34]
                #print(stat14)
                stat15 = stats[15].text
                stat15 = stat15[29:33]
                #print(stat15)

                playerObject = createPlayerObjectGK(Name, Position, Footed, Birthdate, NationalTeam,
                                                       Club, stat1, stat2, stat3, stat4,
                                                       stat5, stat6, stat8, stat9,
                                                       stat10, stat11, stat13, stat14, stat15)
                playersGKs.append(playerObject)                
                
            else:
                #print(Name)
                stats = soup.find_all("tr")
                stat1 = stats[1].text
                stat1 = stat1[17:21]
                #print(stat1)
                stat2 = stats[2].text
                stat2 = stat2[20:24]
                #print(stat2)
                stat3 = stats[3].text
                stat3 = stat3[11:15]
                #print(stat3)
                stat4 = stats[4].text
                stat4 = stat4[7:11]
                #print(stat4)
                stat5 = stats[5].text
                stat5 = stat5[28:32]
                #print(stat5)
                stat6 = stats[6].text
                stat6 = stat6[10:14]
                #print(stat6)
                stat7 = stats[7].text
                stat7 = stat7[21:25]
                #print(stat7)
                stat9 = stats[9].text
                stat9 = stat9[16:20]    
                #print(stat9)     
                stat10 = stats[10].text
                stat10 = stat10[17:22]
                #print(stat10)
                stat11 = stats[11].text
                stat11 = stat11[18:22]
                #print(stat11)
                stat12 = stats[12].text
                stat12 = stat12[19:23]
                #print(stat12)
                stat12 = stats[13].text
                stat12 = stat12[19:23]  
                #print(stat12) 
                stat14 = stats[14].text
                stat14 = stat14[17:21]  
                #print(stat14) 
                stat15 = stats[15].text
                stat15 = stat15[22:26]  
                #print(stat15)        
                stat17 = stats[17].text
                stat17 = stat17[7:11]  
                #print(stat17)     
                stat18 = stats[18].text
                stat18 = stat18[13:17]  
                #print(stat18)     
                stat19 = stats[19].text
                stat19 = stat19[6:10]  
                #print(stat19)     
                stat20 = stats[20].text
                stat20 = stat20[10:14]  
                #print(stat20)     
                stat21 = stats[21].text
                stat21 = stat21[11:15]  
                #print(stat21)              
            
                playerObject = createPlayerObjectNonGK(Name, Position, Footed, Birthdate, NationalTeam,
                                                       Club, stat1, stat2, stat3, stat4,
                                                       stat5, stat6, stat7, stat9, stat10,
                                                       stat11, stat12, stat14, stat15, stat17,
                                                       stat18, stat19, stat20, stat21)
                playersNonGK.append(playerObject)

            time.sleep(2)

    return playersNonGK, playersGKs


if __name__ == '__main__':
    print("main")

    teamUrls = getTeamUrls()
    #print(teamUrls)
    
    NonGKs, GKs = retrievePlayerStats(teamUrls[0:2])
    print("-----------------NonGKs-----------------------------------")
    for x in range (len(NonGKs)):
        print(NonGKs[x]["name"], end = " ")
        print(NonGKs[x]["nationality"], end = " ")
        print(NonGKs[x]["club"])

    print("-----------------GoalKeepers-----------------------------------")
    for x in range (len(GKs)):
        print(GKs[x]["name"], end = " ")
        print(GKs[x]["nationality"], end = " ")
        print(GKs[x]["club"])