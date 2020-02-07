import csv
all_text_file_info = []
with open('gameURLsOrganizedFrom1998to2015.csv', 'r') as f:
    reader = csv.reader(f)
    all_text_file_info = list(reader)
all_text_file_info
for x in all_text_file_info:
    if x[5] == '2010':
        x[2]
'/boxes/BOS/BOS201004040.shtml'
