import csv
import numpy as np


def transform(file_path):
    """transform xyz csv file into data

    :param file_path: xyz file path of csv file
    :return: array of tuple data
    """
    data_xyz = np.empty((11, 11, 13), dtype=object)
    with open(file_path) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            try:
                x = int(row[0])
                y = int(row[1])
                z = int(row[2])
                if row[3] != '-':
                    way = int(row[5])
                    try:
                        addresses = row[4].split('-')
                        data_xyz[x, y, z] = (way, int(row[3]), int(addresses[0]), int(addresses[1]))
                    except ValueError:
                        universes = row[3].split('/')
                        addresses = row[4].split('/')
                        addresses_1 = addresses[0].split('-')
                        addresses_2 = addresses[1].split('-')
                        data_xyz[x, y, z] = (way,
                                             int(universes[0]), int(addresses_1[0]), int(addresses_1[1]),
                                             int(universes[1]),
                                             int(addresses_2[0]),
                                             int(addresses_2[1]))
            except Exception as e:
                print(str(e))
                print(f"Error when parsing {file_path}, Check file pls")
                raise
        return data_xyz
