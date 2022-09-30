from cgitb import text
from html.entities import name2codepoint
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd

# website url

headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://www.pro-football-reference.com/years/2022/"
url_offense = "https://www.pro-football-reference.com/years/2022/advanced.htm"
url_defense = "https://www.nfl.com/stats/team-stats/defense/passing/2022/reg/all"
# send get  request to url
result = req.get(url, headers = headers)
result_offense = req.get(url_offense, headers = headers)
result_defense = req.get(url_defense, headers = headers)

# stores the requested html 
doc = bs(result.text, "html.parser")
offense = bs(result_offense.text, "html.parser")
defense = bs(result_defense.text, "html.parser")

# win loss stats
name_array = []
wins_array = []
losses_array  = []

# offense stats
completed_array = []
attempted_array = []
yards_array = []

# defense stats 
nflNames = []
sack_holder = [] #haha
sackArray = []


team_names = doc.find_all('th')
team_stats = doc.find_all('td')



offense_stats = offense.find_all('td')


club_shortname = defense.select('div[class="d3-o-club-shortname"]')
table_cell = defense.find_all('td')


for i in team_names:
    #stats_array.append(i.get('data-stat'))
    if i.get('data-stat') == "team":
        name_array.append(i.string)

for i in team_stats:
    if i.get('data-stat') == "losses":
        losses_array.append(i.string)

for i in team_stats:
    if i.get('data-stat') == "wins":
        wins_array.append(i.string)

for i in offense_stats:
    if i.get('data-stat') == "pass_cmp":
        completed_array.append(i.string)

for i in offense_stats:
    if i.get('data-stat') == "pass_att":
        attempted_array.append(i.string)

for i in offense_stats:
    if i.get('data-stat') == "pass_yds":
        yards_array.append(i.string)


# defense loops
for i in club_shortname:
    nflNames.append(i.string)

for i in table_cell:
    if i.string != None:
        sack_holder.append(i.string)

count = 1
for i in sack_holder:
    if count <= 10:
        if count == 10:
            sackArray.append(i)
        count += 1
    if count == 11:
        count = 1




# Remove misc text from team names
name_array.remove('Tm')
name_array.remove('Tm')
# No idea why but the original offense arrays were 4x too long
completed = []
attempted = [] 
yards = []

for i in range(0,32):
    completed.append(completed_array[i])

for i in range(0,32):
    attempted.append(attempted_array[i])

for i in range(0,32):
    yards.append(yards_array[i])



data = { 'Teams' : name_array,
         'Wins'  : wins_array,
         'Losses': losses_array,
         'Alphabetical Names': sorted(name_array),
         'Passes Completed' : completed,
         'Passes Attempted' : attempted,
         'Passing Yards'    : yards,
         'NFL Teams(.com order)': nflNames,
         'Sacks' : sackArray}
         
df = pd.DataFrame(data, columns = ['Teams', 'Wins', 'Losses','Alphabetical Names', 'Passes Completed', 'Passes Attempted', 'Passing Yards','NFL Teams(.com order)', 'Sacks'])

df.to_excel(r'C:\Users\fordc\Desktop\export_data_frame.xlsx', index = False, header = True)