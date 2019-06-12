import copy


def transform(file_path):
    data_face = []
    with open(file_path) as data:
        square = 0
        square_array = []
        for x in data:
            s = x.split('|')
            try:
                universe1 = int(s[3])
                if s[4] == '':
                    address1 = 0
                    address2 = 0
                else:
                    a = s[4].split('-')
                    address1 = int(a[0])
                    address2 = int(a[1]) + 1

                square_array.append((universe1, address1, address2))
            except ValueError:
                u = s[3].split('/')
                if len(u) == 2:
                    universe1 = int(u[0])
                    universe2 = int(u[1])
                    if s[4] == '':
                        address1 = 0
                        address2 = 0
                        address3 = 0
                        address4 = 0
                    else:
                        a = s[4].split('/')
                        a1 = a[0]
                        a2 = a[1]
                        a = a1.split('-')
                        address1 = int(a[0])
                        address2 = int(a[1]) + 1
                        a = a2.split('-')
                        address3 = int(a[0])
                        address4 = int(a[1]) + 1
                    square_array.append((universe1, address1, address2, universe2, address3, address4))
                else:
                    square_array.append((-1, -1, -1))
            square += 1
            if square % 4 == 0:
                data_face.append(copy.deepcopy(square_array))
                square_array.clear()

    return data_face
