from lib.StupidArtnet import StupidArtnet
from lib.ArtNetGroup import ArtNetGroup
import time

ledstrip_data = [[[(0, 0), (0, 81), (0, 162)]], [], [], [], [], []]

print(ledstrip_data[0][0][1][1] + 12)
port = 6454
ip = '192.168.0.50'
group = ArtNetGroup()
tab_parabole = []
for x in range(150):
    tab_parabole.append(int(-x * (x - 255) / 63.75))

for i in range(100):
    a = StupidArtnet(ip, port, i)
    a.flash_all()
    group.add(a)

group.start(False)
time.sleep(100)
flash = True
for d in range(5):

    for i in group.listArtNet:
        if flash:
            i.blackout()
        else:
            i.flash_all()
    flash = not flash
    time.sleep(2)
time.sleep(2)
for d in range(255):

    for i in group.listArtNet:
        i.fade_in()

    time.sleep(0.05)

for d in range(255):

    for i in group.listArtNet:
        i.fade_out()

    # flash = not flash

    time.sleep(0.05)
time.sleep(2)
for d in tab_parabole:

    for i in group.listArtNet:
        i.parabole(d)

    # flash = not flash

    time.sleep(0.05)

time.sleep(3)
group.stop()
