import csv


def transform(file_path):
    data_xyz = [[[(None, None, None) for z in range(13)] for y in range(11)] for x in range(11)]
    with open(file_path) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            try:
                x = int(row[0])
                y = int(row[1])
                z = int(row[2])

                try:
                    if row[3] != '-':
                        addresses = row[4].split('-')
                        data_xyz[x][y][z] = (int(row[3]), int(addresses[0]), int(addresses[1]))
                except ValueError:
                    universes = row[3].split('/')
                    addresses = row[4].split('/')
                    addresses_1 = addresses[0].split('-')
                    addresses_2 = addresses[1].split('-')
                    data_xyz[x][y][z] = (
                        int(universes[0]), int(addresses_1[0]), int(addresses_1[1]), int(universes[1]),
                        int(addresses_2[0]),
                        int(addresses_2[1]))
            except:
                print("Error when parsing xyz.csv in package/import_data/data. Check file pls")

        return data_xyz
