
import requests
import re
from bs4 import BeautifulSoup, Comment
import os
import itertools
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
    baseball_table_batter_stats = soup.find_all('tr')
    for b in baseball_table_batter_stats:
        # 1st layer filter
        if(hasattr(b, "contents") and hasattr(b.contents[0], "attrs")):
            # second layer filter for player detection
            if('data-stat' in b.contents[0].attrs and b.contents[0].attrs['data-stat'] == 'player'):
                # filter for batting against team totals and pitching
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
                    all_batters.append(single_batter)
    return all_batters


def getPitchingStats():
    all_pitchers = []
    baseball_table_pitcher_stats = soup.find_all('tr')
    for b in baseball_table_pitcher_stats:
        # 1st layer filter
        if(hasattr(b, "contents") and hasattr(b.contents[0], "attrs")):
            # second layer filter for player detection
            if('data-stat' in b.contents[0].attrs and b.contents[0].attrs['data-stat'] == 'player'):
                # filter for batting against team totals and pitching
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
                    all_pitchers.append(single_pitcher)
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
            lineups_final.append(lineups_temp[:x+1])
            lineups_final.append(lineups_temp[x+1:])
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
    metaInfo.append(meta_info_state[0].contents[1].text.split(',')[
                    0])  # day of week
    metaInfo.append(meta_info_state[0].contents[1].text.split(',')[
                    1])  # month and day
    metaInfo.append(meta_info_state[0].contents[1].text.split(',')[
                    2])  # year
    metaInfo.append(
        meta_info_state[0].contents[2].text.split(':', 1)[1].strip().split(' ')[0])  # time
    metaInfo.append(
        meta_info_state[0].contents[2].text.split(':', 1)[1].strip().split(' ')[1])  # time
    metaInfo.append(meta_info_state[0].contents[3].text.split(':')[
                    1].replace(',', ''))  # attendance
    metaInfo.append(meta_info_state[0].contents[4].text.split(':')[1])  # field
    metaInfo.append(meta_info_state[0].contents[5].text.split(
        ':', 1)[1])  # game duration
    # night/day game, field type
    metaInfo.append(meta_info_state[0].contents[6].text.split(',')[0])
    metaInfo.append(meta_info_state[0].contents[6].text.split(',')[1])
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
    startWeather = []
    weather_info_stats = soup.find_all(class_='section_content')
    weatherLen = len(weather_info_stats[2].contents[6].contents[1].split(','))
    for x in range(0, weatherLen):
        startWeather.append(
            weather_info_stats[2].contents[6].contents[1].split(',')[x].replace('.', '').strip())
    startWeather[0] = re.findall(r'\d+', startWeather[0])[0]
    startWeather.append(re.findall(r'\d+', startWeather[1])[0])
    return startWeather
    #startWeatherLen = len(weather_info_stats)


r = requests.get(
    'https://www.baseball-reference.com/boxes/SLN/SLN201804080.shtml')
print(r.ok)
print(r.status_code)

# http://www.parkfactors.com/MLW
comments_removed_text = (r.text.replace('<!--', '')).replace('-->', '')
soup = BeautifulSoup(comments_removed_text, 'html.parser')
print(getTeamsAndScores())
print(getPreviousAndNextGameURLs())
print(getScoreboxMeta())
print(getUmpires())
print(getStartTimeWeather())
print(getBattingStats())
print(getPitchingStats())
print(getStartingLineups())
