

path = 'D:\\Baseball\\Database\\Weather\\'
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            filename = file.split('_')[0]
            all_file_names.remove(filename)
