
from unidecode import unidecode
import requests
from bs4 import BeautifulSoup
import pandas as pd

Championship = "https://fbref.com/en/comps/23/Eredivisie-Stats"

data = requests.get(Championship)
soup = BeautifulSoup(data.text, features = "html.parser")

table = soup.select('table', class_='stats_table')[0]

#print(len(table))
links = table.find_all('a')
print(links)
#print(table[0])