import os
import itertools
import csv
import time
import datetime

textFiles = [os.path.join(root, name)
             for root, dirs, files in os.walk("D:/Dropbox (MIT)/Portfolio/In Progress/Baseball Data/OldInfo/Games Played by Team")
             for name in files
             if name.endswith((".text"))]

all_text_file_info = []

for x in textFiles:
    f = open(x, "r")
    fileContents = f.read()
    fileContents = fileContents.split('\n')
    for y in fileContents:
        if(len(y) > 0):
            j = y.split(',')
            j.extend(j[1].split('-'))
            dt = datetime.datetime.strptime(j[1], '%Y-%m-%d')
            j.append(time.mktime(dt.timetuple()))
            all_text_file_info.append(j)


def Sort(sub_li):

    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    return(sorted(sub_li, key=lambda x: x[8]))


all_text_file_info.sort()
"""
all_text_file_info = list(all_text_file_info for all_text_file_info,
                          _ in itertools.groupby(all_text_file_info))
                          """
seen = set()

all_text_file_info = [x for x in all_text_file_info if x[2]
                      not in seen and not seen.add(x[2])]

all_text_file_info = Sort(all_text_file_info)
with open("gameURLsOrganizedFrom1998to2015.csv", "w", newline='') as f:
    wr = csv.writer(f)
    wr.writerows(all_text_file_info)
