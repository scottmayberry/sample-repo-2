
import requests
from bs4 import BeautifulSoup, Comment


r = requests.get(
    'https://www.baseball-reference.com/boxes/ARI/ARI201806010.shtml')
print(r.ok)
print(r.status_code)

text_without_first_comment_string = r.text.replace('<!--', '')
finalText = text_without_first_comment_string.replace('-->', '')


soup = BeautifulSoup(finalText, 'html.parser')
score_list_identifier = soup.find(
    class_='linescore_wrap')
score_list = score_list_identifier.find_all('td')


baseball_table_1_identifier = soup.find(class_='table_outer_container')
baseball_table_1_player_stats = soup.find_all('tr')
for b in baseball_table_1_player_stats:
    # 1st layer filter
    if(hasattr(b, "contents") and hasattr(b.contents[0], "attrs")):
        # second layer filter for player detection
        if('data-stat' in b.contents[0].attrs and b.contents[0].attrs['data-stat'] == 'player'):
            # filter for batting against team totals and pitching
            if('data-append-csv' in b.contents[0].attrs and b.contents[1].attrs['data-stat'] == 'AB'):
                print(b.contents[0].attrs['data-append-csv'])
                # get url (in different position for some people)
                for x in range(0, len(b.contents[0].contents)):
                    if(hasattr(b.contents[0].contents[x], "attrs")):
                        print(b.contents[0].contents[x].attrs['href'])
                        break
                for i in range(1, len(b.contents)):
                    if(len(b.contents[i].contents) != 0):
                        print(b.contents[i].contents[0])
                    else:
                        print("none")
    # b.contents[14].attrs.contents[0]


"""
Batting Table 1
short id name..........var.contents[0].attrs['data=append-csv']
URL....................var.contents[0].contents[0]['href']
at bat.................var.contents[1].attrs.contents[0]
runs scored/allowed....var.contents[2].attrs.contents[0]
hits/hits allowed......var.contents[3].attrs.contents[0]
runs batted in.........var.contents[4].attrs.contents[0]
bases on balls/walks...var.contents[5].attrs.contents[0]
strikeouts.............var.contents[6].attrs.contents[0]
plate appearances......var.contents[7].attrs.contents[0]
batting average........var.contents[8].attrs.contents[0]
on base percentage.....var.contents[9].attrs.contents[0]
SLG....................var.contents[10].attrs.contents[0]
on-base + slug perc....var.contents[11].attrs.contents[0]
pitches................var.contents[12].attrs.contents[0]
strikes................var.contents[13].attrs.contents[0]
WPA....................var.contents[14].attrs.contents[0]
aLI....................var.contents[15].attrs.contents[0]
WPA+...................var.contents[16].attrs.contents[0]
WPA-...................var.contents[17].attrs.contents[0]
RE24...................var.contents[18].attrs.contents[0]
putouts................var.contents[19].attrs.contents[0]
assists................var.contents[20].attrs.contents[0]
details................var.contents[21].attrs.contents[0]
"""
