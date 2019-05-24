from lib.StupidArtnet import StupidArtnet
from lib.ArtNetGroup import ArtNetGroup
import time

test = bytearray(512)

# print(test)

test = [i + 1 for i in test]

# print(test)

port = 6454
ip = '192.168.1.142'
group = ArtNetGroup()

for i in range(1):
    a = StupidArtnet(ip, port, i)
    group.add(a)

ledstrip_data = [[[(group.listArtNet[0].BUFFER, 0, 81, -1, -1, -1), (0, 162)]], [], [], [], [], []]

print(ledstrip_data[0][0][0][0][0])
print(group.listArtNet[0].BUFFER[0])
ledstrip_data[0][0][0][0][0] = 14

print(ledstrip_data[0][0][0][0][0])
print(group.listArtNet[0].BUFFER[0])
