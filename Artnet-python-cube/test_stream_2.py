from lib.StupidArtnet import StupidArtnet
from lib.ArtNetGroup import ArtNetGroup
import time

ledstrip_data = [[[(0, 0), (0, 81), (0, 162)]], [], [], [], [], []]

print(ledstrip_data[0][0][1][1] + 12)
port = 6454
ip = '157.26.105.127'
group = ArtNetGroup()
r = 2
tab_parabole = []
for x in range(256):
    tab_parabole.append(int(-x * (x - 255) / 63.75))

for i in range(91):
    a = StupidArtnet(ip, port, i)
    group.add(a)

for i in range(r):
    group.listArtNet[i].flash_all()

group.start(True)
time.sleep(2)
flash = True
for d in range(5):

    for i in range(r):
        if flash:
            group.listArtNet[i].blackout()
        else:
            group.listArtNet[i].flash_all()
    flash = not flash
    time.sleep(2)

for d in range(255):

    for i in range(r):
        group.listArtNet[i].fade_in()

    time.sleep(0.01)

for d in range(255):

    for i in range(r):
        group.listArtNet[i].fade_out()

    # flash = not flash

    time.sleep(0.01)

for d in tab_parabole:

    for i in range(r):
        group.listArtNet[i].parabole(d)

    # flash = not flash

    time.sleep(0.01)

time.sleep(3)
group.stop()
