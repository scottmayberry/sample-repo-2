
import requests
import re
from bs4 import BeautifulSoup, Comment
import os
import itertools
import csv
import time
import math
print(os.getcwd())


def getBattingStats():
    """
    Batting Table 1
    short id name..........var.contents[0].attrs['data=append-csv']
    URL....................var.contents[0].contents[x]['href']
    name...................var.contents[0].contents[x].text
    at bat.................var.contents[1].contents[0]
    runs scored/allowed....var.contents[2].contents[0]
    hits/hits allowed......var.contents[3].contents[0]
    runs batted in.........var.contents[4].contents[0]
    bases on balls/walks...var.contents[5].contents[0]
    strikeouts.............var.contents[6].contents[0]
    plate appearances......var.contents[7].contents[0]
    batting average........var.contents[8].contents[0]
    on base percentage.....var.contents[9].contents[0]
    SLG....................var.contents[10].contents[0]
    on-base + slug perc....var.contents[11].contents[0]
    pitches................var.contents[12].contents[0]
    strikes................var.contents[13].contents[0]
    WPA....................var.contents[14].contents[0]
    aLI....................var.contents[15].contents[0]
    WPA+...................var.contents[16].contents[0]
    WPA-...................var.contents[17].contents[0]
    RE24...................var.contents[18].contents[0]
    putouts................var.contents[19].contents[0]
    assists................var.contents[20].contents[0]
    details................var.contents[21].contents[0]
    """
    all_batters = []
    one_team_batters = []
    baseball_table_batter_stats = soup.find_all('tr')
    for b in baseball_table_batter_stats:
        # 1st layer filter
        if(hasattr(b, "contents") and hasattr(b.contents[0], "attrs")):
            # second layer filter for player detection
            if('data-stat' in b.contents[0].attrs and b.contents[0].attrs['data-stat'] == 'player'):
                # filter for batting against team totals and pitching
                if('Team Totals' in b.contents[0].text and len(one_team_batters) > 0):
                    all_batters.append(one_team_batters.copy())
                    one_team_batters = []
                if('data-append-csv' in b.contents[0].attrs and b.contents[1].attrs['data-stat'] == 'AB'):
                    single_batter = []
                    single_batter.append(
                        b.contents[0].attrs['data-append-csv'])
                    # get url (in different position for some people)
                    for x in range(0, len(b.contents[0].contents)):
                        if(hasattr(b.contents[0].contents[x], "attrs")):
                            single_batter.append(
                                b.contents[0].contents[x].text)
                            single_batter.append(
                                b.contents[0].contents[x].attrs['href'])
                            break
                    for i in range(1, len(b.contents)):
                        if(len(b.contents[i].contents) != 0):
                            single_batter.append(b.contents[i].contents[0])
                        else:
                            single_batter.append("none")
                    one_team_batters.append(single_batter)
    all_batters.append(one_team_batters)
    return all_batters


def getPitchingStats():
    all_pitchers = []
    one_team_pitchers = []
    baseball_table_pitcher_stats = soup.find_all('tr')
    for b in baseball_table_pitcher_stats:
        # 1st layer filter
        if(hasattr(b, "contents") and hasattr(b.contents[0], "attrs")):
            # second layer filter for player detection
            if('data-stat' in b.contents[0].attrs and b.contents[0].attrs['data-stat'] == 'player'):
                # filter for batting against team totals and pitching
                if('Team Totals' in b.contents[0].text and len(one_team_pitchers) > 0):
                    all_pitchers.append(one_team_pitchers.copy())
                    one_team_pitchers = []
                if('data-append-csv' in b.contents[0].attrs and b.contents[1].attrs['data-stat'] == 'IP'):
                    single_pitcher = []
                    single_pitcher.append(
                        b.contents[0].attrs['data-append-csv'])
                    # get url (in different position for some people)
                    for x in range(0, len(b.contents[0].contents)):
                        if(hasattr(b.contents[0].contents[x], "attrs")):
                            single_pitcher.append(
                                b.contents[0].contents[x].text)
                            single_pitcher.append(
                                b.contents[0].contents[x].attrs['href'])
                            break
                    for i in range(1, len(b.contents)):
                        if(len(b.contents[i].contents) != 0):
                            single_pitcher.append(b.contents[i].contents[0])
                        else:
                            single_pitcher.append("none")
                    one_team_pitchers.append(single_pitcher)
    all_pitchers.append(one_team_pitchers)
    return all_pitchers


def getStartingLineups():
    lineups_final = []
    lineups_temp = []
    lineup_table_stats = soup.find_all('table')
    for lu in lineup_table_stats:
        # has contents attribute and the length is large enough to be a lineup
        if(hasattr(lu, "contents") and len(lu.contents) > 10):
            for x in range(0, len(lu.contents)):
                if(hasattr(lu.contents[x], "contents")):
                    single_lineup = []
                    for y in range(0, len(lu.contents[x])):
                        if(hasattr(lu.contents[x].contents[y], "contents")):
                            for j in range(0, len(lu.contents[x].contents[y])):
                                if(hasattr(lu.contents[x].contents[y].contents[j], "contents")):
                                    for h in range(0, len(lu.contents[x].contents[y].contents[j])):
                                        single_lineup.append(
                                            lu.contents[x].contents[y].contents[j].contents[h])
                                    single_lineup.append(
                                        lu.contents[x].contents[y].contents[j].attrs['href'])
                                else:
                                    single_lineup.append(
                                        lu.contents[x].contents[y].contents[j])
                    lineups_temp.append(single_lineup)
    lineups_temp = [x for x in lineups_temp if x != []]
    for x in range(0, len(lineups_temp)):
        if(lineups_temp[x][0] == '9'):
            adj = 0
            if(lineups_temp[x+1][0] == ' '):
                adj = 1
            lineups_final.append(lineups_temp[:x+1+adj])
            lineups_final.append(lineups_temp[x+1+adj:])
            break
    return lineups_final


def getTeamsAndScores():
    all_teams = []
    all_teams_stats = soup.find_all(itemprop='performer')
    # teams links and names grabbing
    for x in range(0, len(all_teams_stats)):
        single_team = []
        single_team.append(
            all_teams_stats[x].contents[3].contents[1].attrs['href'])
        single_team.append(single_team[0].split('/')[2])
        single_team.append(all_teams_stats[x].contents[3].contents[1].text)
        all_teams.append(single_team)
    # scores grabbing
    all_scores_stats = soup.find_all(class_='score')
    for x in range(0, len(all_scores_stats)):
        all_teams[x].append(all_scores_stats[x].text)
    return all_teams


def getPreviousAndNextGameURLs():
    gameURLS = []
    game_urls_stats = soup.find_all(class_='prevnext')
    for x in range(0, len(game_urls_stats)):
        single_gameURLS = [None]*2
        for y in game_urls_stats[x].contents:
            if(hasattr(y, "contents")):
                if(y.text == 'Prev Game'):
                    single_gameURLS[0] = y.attrs['href']
                elif(y.text == 'Next Game'):
                    single_gameURLS[1] = y.attrs['href']
        gameURLS.append(single_gameURLS)
    return gameURLS


def getScoreboxMeta():
    metaInfo = []
    meta_info_state = soup.find_all(class_='scorebox_meta')
    for x in meta_info_state[0].contents:
        if(hasattr(x, 'contents')):
            metaInfo.append(x.text)
    for x in range(0, len(metaInfo)):
        metaInfo[x] = metaInfo[x].strip()
    return metaInfo


def getUmpires():
    umpires = []
    meta_info_state = soup.find_all(class_='section_content')
    umpiresLen = len(meta_info_state[2].contents[1].contents[1].split(','))
    for x in range(0, umpiresLen):
        umpires.append(
            meta_info_state[2].contents[1].contents[1].split(',')[x].split('-')[1].replace('.', '').strip())
    return umpires


def getStartTimeWeather():
    weather_info_stats = soup.find_all(class_='section_content')
    for x in range(0, len(weather_info_stats[2].contents)):
        if(hasattr(weather_info_stats[2].contents[x], "content") and "Weather" in weather_info_stats[2].contents[x].text):
            return weather_info_stats[2].contents[x].text
    #startWeatherLen = len(weather_info_stats)


def saveFileToCSV(fileLocation, tag, data):
    with open(fileLocation, "w+", newline='') as f:
        wr = csv.writer(f)
        wr.writerow([tag])
        wr.writerows(data)


def addToErrorFile(databaseLocation, urlName):
    with open(databaseLocation + "errors/readErrors.csv", "a+", newline='') as f:
        wr = csv.writer(f)
        wr.writerow([urlName])


databaseLocation = "D:/Baseball/Database/"
delay_time = 3.2

all_text_file_info = []
with open('gameURLsOrganizedFrom1998to2015.csv', 'r') as f:
    reader = csv.reader(f)
    all_text_file_info = list(reader)
all_text_file_info
counter = 0
for x in all_text_file_info:
    counter += 1
    baseball_reference_static = 'https://www.baseball-reference.com'
    request_string = baseball_reference_static + x[2]
    #request_string = "https://www.baseball-reference.com/boxes/SEA/SEA199803310.shtml"
    print(str(counter) + ": " + request_string)
    request_time = time.time()
    try:
        r = requests.get(
            request_string)
        print(r.ok)
        print(r.status_code)
        # http://www.parkfactors.com/MLW
        comments_removed_text = (
            r.text.replace('<!--', '')).replace('-->', '')
        soup = BeautifulSoup(comments_removed_text, 'html.parser')
        teamAndScores = getTeamsAndScores()
        previousAndNextGameURLs = getPreviousAndNextGameURLs()
        for z in range(0, len(previousAndNextGameURLs)):
            teamAndScores[z].append(previousAndNextGameURLs[z][0])
            teamAndScores[z].append(previousAndNextGameURLs[z][1])
        meta = getScoreboxMeta()
        umpires = getUmpires()
        startTimeWeather = getStartTimeWeather()
        battingStats = getBattingStats()
        pitchingStats = getPitchingStats()
        startingLineups = getStartingLineups()
        fileNameBase = request_string.split('/')[5].split('.')[0]
        # print(fileNameBase)
        saveFileToCSV(databaseLocation + "teamAndScores/" + fileNameBase +
                      "_teamAndScores.csv", x[2], teamAndScores)
        saveFileToCSV(databaseLocation + "Meta/" + fileNameBase +
                      "_meta.csv", x[2], [meta])
        saveFileToCSV(databaseLocation + "Umpires/" + fileNameBase +
                      "_umpires.csv", x[2], [umpires])
        saveFileToCSV(databaseLocation + "Weather/" + fileNameBase +
                      "_weather.csv", x[2], [[startTimeWeather]])
        saveFileToCSV(databaseLocation + "startingLineups/" + fileNameBase +
                      "_startingLineups.csv", x[2], startingLineups)
        saveFileToCSV(databaseLocation + "Pitching/" + fileNameBase +
                      "_pitching.csv", x[2], pitchingStats)
        saveFileToCSV(databaseLocation + "Batting/" + fileNameBase +
                      "_batting.csv", x[2], battingStats)
        with open(databaseLocation + "html/" + fileNameBase +
                  "_html.txt", "w+", buffering=-1, encoding='utf-8') as f:
            # print(soup.getText())
            f.writelines(comments_removed_text)
    except:
        addToErrorFile(databaseLocation, request_string)
    time_in_between_read = time.time() - request_time
    if(time_in_between_read < delay_time):
        time.sleep(delay_time - math.floor(time_in_between_read))
