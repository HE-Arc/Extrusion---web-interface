import sys

sys.path.append(".")
from lib.StupidArtnet import StupidArtnet
from lib.StupidArtSync import StupidArtSync
from lib.animation.animation import Animation
import time
import datetime

filename = "tests/logs/dynamic/test3.txt"
file = open(filename, "a")


def main_no_artsync(universe1, universe2, ip1='127.0.0.1', ip2='127.0.0.1', tmp=0.5):
    packet_size = 512
    port = 6454
    a1 = StupidArtnet(ip1, port, universe1, packet_size)
    a2 = StupidArtnet(ip2, port, universe2, packet_size)
    anim = Animation(filename, a1, a2)
    anim.anime_noartsync(Animation.anime_1, tmp)


def main_artsync(universe1, universe2, ip1='127.0.0.1', ip2='127.0.0.1', tmp=0.5):
    packet_size = 512
    port = 6454
    a1 = StupidArtnet(ip1, port, universe1, packet_size)
    a2 = StupidArtnet(ip2, port, universe2, packet_size)
    anim = Animation(filename, a1, a2)
    anim.anime_artsync(Animation.anime_1, tmp)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = sys.argv[1]
        ip1 = sys.argv[2]
        ip2 = sys.argv[3]
        universe1 = sys.argv[4]
        universe2 = sys.argv[5]
        time = sys.argv[6]

        file.write(f"\n{type}")
        file.write(f" test starting: {datetime.datetime.now()}")

        print(f"Animate universe: {universe1} on ip {ip1}, {universe2} on ip {ip2}")
        if type == "noartsync":
            main_no_artsync(int(universe1), int(universe2), ip1, ip2, float(time))
        elif type == "artsync":
            main_artsync(int(universe1), int(universe2), ip1, ip2, float(time))
        file.write(f"test ending: {datetime.datetime.now()}\n")
    else:
        print("Wrong arguments,arguments: type , ip1, ip2, universe1, universe2, animation_time")

    file.close()
