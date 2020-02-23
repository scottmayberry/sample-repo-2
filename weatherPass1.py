import csv
import os

path = 'D:\\Baseball\\Database\\Weather\\'
all_file_names = []
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            all_file_names.append(file)

all_data_of_weather = []
for x in all_file_names:
    with open(path+x, "r", newline='') as f:
        reader = csv.reader(f)
        all_text_file_info = list(reader)
        temp = [all_text_file_info[0][0]]
        temp.extend(all_text_file_info[1][0].split(':')[1].split(','))
        for y in temp:
            y = y.strip()
        all_data_of_weather.append(temp)

path2 = 'D:\\Baseball\\Database\\Weather_Pass_1\\'
for x in range(0, len(all_file_names)):
    with open(path2+all_file_names[x], "w+", newline='') as f:
        wr = csv.writer(f)
        wr.writerows([all_data_of_weather[x]])
