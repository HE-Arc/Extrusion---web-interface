from lib.StupidArtnet import StupidArtnet
from lib.ArtNetGroup import ArtNetGroup
import time

ledstrip_data = [[[(0, 0), (0, 81), (0, 162)]], [], [], [], [], []]

print(ledstrip_data[0][0][1][1] + 12)
port = 6454
ip = '157.26.105.127'
group = ArtNetGroup()
tab_parabole = []
for x in range(256):
    tab_parabole.append(int(-x * (x - 255) / 63.75))

for i in range(50):
    a = StupidArtnet(ip, port, i)
    group.add(a)

group.listArtNet[0].flash_all()
group.start(True)
time.sleep(2)
flash = True
for d in range(5):

    if flash:
        group.listArtNet[0].blackout()
    else:
        group.listArtNet[0].flash_all()
    flash = not flash
    time.sleep(2)

for d in range(255):
    group.listArtNet[0].fade_in()

    time.sleep(0.01)

for d in range(255):
    group.listArtNet[0].fade_out()

    # flash = not flash

    time.sleep(0.01)

for d in tab_parabole:
    group.listArtNet[0].parabole(d)

    # flash = not flash

    time.sleep(0.01)

time.sleep(3)
group.stop()
