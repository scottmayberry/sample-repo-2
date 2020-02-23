import csv
import os


def addToWeatherFile(databaseLocation, dataLine):
    with open(databaseLocation, "a+", newline='') as f:
        wr = csv.writer(f)
        wr.writerow([dataLine])


def saveFileToCSV(fileLocation, dataUpdate):
    with open(fileLocation, "w+", newline='') as f:
        wr = csv.writer(f)
        wr.writerows(dataUpdate)


path = 'D:\\Baseball\\Database\\Weather\\'
linksToData = []

for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            linksToData.append(os.path.join(r, file))

pathToSave = "D:/Baseball/Database/weather_condition_types.csv"
windData = []

# In Dome = no wind and stable temp
# Overcast = no wind data


for fileLocation in linksToData:
    with open(fileLocation, "r", newline='') as f:
        reader = csv.reader(f)
        windText = fileLocation
        try:
            windText = list(reader)[1][0]
            windText = windText.split(':')[1].split(',')[1].strip()
            if('mph' in windText and ' 0mph' not in windText):
                windText = windText.split('mph')[1].strip()
            # if('Overcast' in windText):
            #    windText = fileLocation
        except:
            pass
        windData.append(windText)

windData = list(set(windData))
saveFileToCSV(pathToSave, [windData])

#saveFileToCSV(pathToSave, data)
