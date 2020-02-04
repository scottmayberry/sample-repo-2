import csv
all_text_file_info = []
with open('gameURLsOrganizedFrom1998to2015.csv', 'r') as f:
    reader = csv.reader(f)
    all_text_file_info = list(reader)
all_text_file_info
