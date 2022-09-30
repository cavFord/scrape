from cgitb import text
from html.entities import name2codepoint
from re import T
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd

# website url

headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://www.nfl.com/stats/team-stats/defense/passing/2022/reg/all"

# send get  request to url
result = req.get(url, headers = headers)
# stores the requested html 
doc = bs(result.text, "html.parser")

teamArray = []
pointsArray = []
sacksArray = []

teams = doc.find_all('td')

test = doc.select('div[class="d3-o-club-shortname"]')

for i in test:
    teamArray.append(i.string)

for i in teams:
    print(i.contents)


for i in teams:
    if i.string != None:
        pointsArray.append(i.string)

count = 1
for i in pointsArray:
    if count <= 10:
        if count == 10:
            sacksArray.append(i)
        count += 1
    if count == 11:
        count = 1

print(pointsArray)
print(sacksArray)
print(len(sacksArray))
