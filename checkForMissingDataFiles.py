import csv
import os


all_text_file_info = []
with open('gameURLsOrganizedFrom1998to2015.csv', 'r') as f:
    reader = csv.reader(f)
    all_text_file_info = list(reader)
all_file_names = []
for x in all_text_file_info:
    all_file_names.append(x[2].split('/')[3].split('.')[0].strip())

path = 'D:\\Baseball\\Database\\Batting\\'
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            filename = file.split('_')[0]
            all_file_names.remove(filename)
all_file_names
