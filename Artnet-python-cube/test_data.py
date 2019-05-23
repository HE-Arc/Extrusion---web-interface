from lib.StupidArtnet import StupidArtnet
from lib.ArtNetGroup import ArtNetGroup
import time
ledstrip_data = [[[(0, 0), (0, 81), (0, 162)]], [], [], [], [], []]

print(ledstrip_data[0][0][1][1] + 12)
port = 6454
ip = '192.168.1.142'
group = ArtNetGroup()

for i in range(91):
    a = StupidArtnet(ip, port, i)
    a.flash_all()
    group.add(a)

group.start(True)
time.sleep(3)
group.stop()

