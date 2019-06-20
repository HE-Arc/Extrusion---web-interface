import csv


def transform(file_path, nb_square):
    data_face = [[(None, None, None) for ledstrip in range(4)] for square in range(nb_square)]
    with open(file_path) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            try:
                square_idx = int(row[0])
                ledstrip_idx = int(row[1])
                try:
                    if row[2] != '-':
                        addresses = row[3].split('-')
                        data_face[square_idx][ledstrip_idx] = (int(row[2]), int(addresses[0]), int(addresses[1]) + 1)
                except ValueError:
                    universes = row[2].split('/')
                    addresses = row[3].split('/')
                    addresses_1 = addresses[0].split('-')
                    addresses_2 = addresses[1].split('-')
                    data_face[square_idx][ledstrip_idx] = (
                        int(universes[0]), int(addresses_1[0]), int(addresses_1[1]) + 1, int(universes[1]),
                        int(addresses_2[0]),
                        int(addresses_2[1]) + 1)
            except:
                print(f"Error when parsing {file_path}. Check file pls")

        return data_face
