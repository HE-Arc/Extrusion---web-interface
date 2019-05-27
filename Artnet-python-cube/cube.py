from lib.StupidArtnet import StupidArtnet
from lib.ArtNetGroup import ArtNetGroup

port = 6454
ip = '192.168.1.142'
group = ArtNetGroup()

for i in range(1):
    a = StupidArtnet(ip, port, i)
    group.add(a)

for i in range(1):
    a = StupidArtnet(ip, port, i)
    group.add(a)


class Cube:
    def __init__(self, *Face):
        self.face = []
        for i in Face:
            self.face.append(i)


class Face:
    def __init__(self, *square):
        self.square = []
        for i in square:
            self.square.append(i)


class Square:
    def __init__(self, *ledstrip):
        self.ledstrip = []
        for i in ledstrip:
            self.ledstrip.append(i)


class Ledstrip:
    def __init__(self, *data):
        self.led = []
        for i in data:
            self.led.append(i)


if __name__ == '__main__':
    ledstrip_test = Ledstrip((a.BUFFER, 0, 80), (a.BUFFER, 81, 161))
    square_test = Square(ledstrip_test)
    face_test = Face(square_test)
    cube_test = Cube(face_test)

    print(cube_test.face[0].square[0].ledstrip[0].led[0][0])
    print(a.BUFFER)

    cube_test.face[0].square[0].ledstrip[0].led[0][0][0] = 12

    print(cube_test.face[0].square[0].ledstrip[0].led[0][0])
    print(a.BUFFER)
