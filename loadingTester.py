import csv
import os
path = 'D:\\Baseball\\Database\\Pitching\\'

all_file_names = []
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            all_file_names.append(file)

all_text_file_info = []
for x in range(0, len(all_file_names)):
    with open(path+all_file_names[x], "r", newline='') as f:
        reader = csv.reader(f)
        all_text_file_info.append(list(reader))

for x in all_text_file_info:
    print(len(x[0]))
