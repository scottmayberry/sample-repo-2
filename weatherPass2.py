import csv
import os


def handleTemperature(temp_string):
    if('Â' in temp_string):
        return temp_string.split('Â')[0].strip()
    else:
        return temp_string.split('°')[0].strip()


def handleWindMPH(mph_string):
    new_value = ''
    temp = mph_string.split(' ')
    for x in temp:
        if('mph' in x):
            new_value = new_value + x.split('mph')[0]
    if(new_value == '0'):
        return new_value
    return new_value + ',' + mph_string.split('mph')[1].strip()


path = 'D:\\Baseball\\Database\\Weather_Pass_1\\'
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
        temp = [None]*9
        for x in all_text_file_info:
            for y in x:
                if('.shtml' in y):
                    temp[0] = y.strip()
                elif('°' in y):
                    temp[1] = handleTemperature(y)
                elif('mph' in y):
                    y = handleWindMPH(y)
                    y = y.split(',')
                    for z in range(0, len(y)):
                        temp[z+2] = y[z]
                elif('recipitation' in y or 'rizzle' in y or 'Rain' in y or 'Showers' in y):
                    if('.' in y):
                        y = y.replace('.', '')
                    temp[4] = y.strip()
                elif('unny' in y or 'loudy' in y or 'vercast' in y or 'ight' in y):
                    temp[5] = y.strip()
                elif('In Dome' in y):
                    temp[6] = 'Dome'
                elif('Unknown' in y):
                    temp[7] = 'Unknown'
                else:
                    print(y)
        all_data_of_weather.append(temp)
path2 = 'D:\\Baseball\\Database\\Weather_Pass_2\\'
for x in range(0, len(all_file_names)):
    with open(path2+all_file_names[x], "w+", newline='') as f:
        wr = csv.writer(f)
        wr.writerows([all_data_of_weather[x]])
